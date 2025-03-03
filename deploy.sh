#!/bin/bash
# azContainerApps_deploy.sh - Enhanced Deployment Script with GitHub Integration

# Define color codes
YELLOW='\033[0;33m'
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Initialize variables
script_dir=$(dirname "$0")
config_found=false
timestamp=$(date +%Y%m%d%H%M%S)
repo_url=""

# Load configuration
dir=$(pwd)
while [[ "$dir" != "/" ]]; do
  if [[ -f "$dir/globalenv.config" ]]; then
    source "$dir/globalenv.config"
    config_found=true
    break
  fi
  dir=$(dirname "$dir")
done

if [ "$config_found" = false ]; then
    echo -e "${RED}Error: globalenv.config not found${NC}"
    exit 1
fi

# Set derived variables
environmentName="${ENVIRONMENT_PREFIX}-${PROJECT_PREFIX}-BackendContainerAppsEnv"
containerAppName="${ENVIRONMENT_PREFIX}-${PROJECT_PREFIX}-worker"
registryUrl="${ENVIRONMENT_PREFIX}${PROJECT_PREFIX}contregistry.azurecr.io"
log_file="${LOG_FOLDER}/deploy_${timestamp}.log"

# Create log directory
mkdir -p "$LOG_FOLDER"

# Redirect output to log file
exec > >(tee -a "$log_file") 2>&1

# Function to validate GitHub repository configuration
validate_github_repo() {
    echo -e "${BLUE}Validating GitHub repository configuration...${NC}"
    
    # Check if we're in a git repository
    if [ ! -d .git ]; then
        echo -e "${RED}Error: Not a git repository. Please initialize git first.${NC}"
        exit 1
    fi

    # Get GitHub repository URL
    repo_url=$(git remote get-url origin 2>/dev/null)
    if [ -z "$repo_url" ]; then
        echo -e "${RED}Error: No GitHub remote found. Please add a remote:"
        echo -e "  git remote add origin https://github.com/Stephen882-pixel/Meru-University-of-Science-and-Technology-WebApp$"
        exit 1
    fi

    # Convert SSH URL to HTTPS if needed
    if [[ "$repo_url" == git@github.com:* ]]; then
        repo_url=$(echo "$repo_url" | sed -e 's/git@github.com:/https:\/\/github.com\//' -e 's/\.git$//')
    fi

    # Verify repo exists and accessible
    if ! gh repo view "$repo_url" >/dev/null 2>&1; then
        echo -e "${RED}Error: Cannot access GitHub repository: $repo_url${NC}"
        exit 1
    fi

    echo -e "${GREEN}GitHub repository configured: ${YELLOW}$repo_url${NC}"
}

# Function to create service principal and store secrets
create_azure_credentials() {
    echo -e "${BLUE}Creating Azure Service Principal...${NC}"
    
    # Create Service Principal with Contributor role
    sp_result=$(az ad sp create-for-rbac --name "${PROJECT_PREFIX}-github-actions-sp" \
        --role contributor \
        --scopes "/subscriptions/${PROJECT_SUBSCRIPTION_ID}/resourceGroups/${PROJECT_RESOURCE_GROUP}" \
        --sdk-auth)
        
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to create service principal${NC}"
        exit 1
    fi

    # Store credentials in GitHub Secrets
    echo -e "${BLUE}Storing credentials in GitHub Secrets...${NC}"
    echo "$sp_result" | gh secret set AZURE_CREDENTIALS --repo "$repo_url"
    gh secret set AZURE_SUBSCRIPTION --body "$PROJECT_SUBSCRIPTION_ID" --repo "$repo_url"
    gh secret set AZURE_RESOURCE_GROUP --body "$PROJECT_RESOURCE_GROUP" --repo "$repo_url"
    gh secret set AZURE_REGISTRY_URL --body "$registryUrl" --repo "$repo_url"
    
    echo -e "${GREEN}Credentials stored in GitHub Secrets${NC}"
}

# Main deployment function
deploy_infrastructure() {
    echo -e "${BLUE}Starting deployment process...${NC}"
    
    # Create Resource Group if not exists
    az group create --name "$PROJECT_RESOURCE_GROUP" \
        --location "$PROJECT_LOCATION" \
        --tags "Environment=${ENVIRONMENT_PREFIX}" "Project=${PROJECT_PREFIX}"
    
    # Deploy core infrastructure
    echo -e "${YELLOW}Deploying Container Apps Environment...${NC}"
    az containerapp env create --name "$environmentName" \
        --resource-group "$PROJECT_RESOURCE_GROUP" \
        --location "$PROJECT_LOCATION"
    
    # Build and deploy application
    echo -e "${YELLOW}Building and deploying container app...${NC}"
    az containerapp up --name "$containerAppName" \
        --resource-group "$PROJECT_RESOURCE_GROUP" \
        --environment "$environmentName" \
        --registry-server "$registryUrl" \
        --ingress external \
        --target-port 8080 \
        --cpu 0.25 \
        --memory 0.5Gi \
        --min-replicas 1 \
        --max-replicas 10
    
    # Update settings
    echo -e "${YELLOW}Finalizing configuration...${NC}"
    az containerapp update --name "$containerAppName" \
        --resource-group "$PROJECT_RESOURCE_GROUP" \
        --set-env-vars "ENVIRONMENT=${ENVIRONMENT_PREFIX}" \
        --cpu 0.25 \
        --memory 0.5Gi
    
    echo -e "${GREEN}Infrastructure deployment completed${NC}"
}

# CI/CD Pipeline Creation
create_cicd_pipeline() {
    echo -e "${BLUE}Creating GitHub Actions workflow...${NC}"
    
    mkdir -p .github/workflows
    cat << EOF > .github/workflows/azure-containerapps-ci.yml
name: Azure Container Apps CI/CD

on:
  push:
    branches: [ "main" ]
  workflow_dispatch:

env:
  RESOURCE_GROUP: "$PROJECT_RESOURCE_GROUP"
  CONTAINERAPP_NAME: "$containerAppName"
  REGISTRY_URL: "$registryUrl"

jobs:
  build-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Azure Login
      uses: azure/login@v1
      with:
        creds: \${{ secrets.AZURE_CREDENTIALS }}

    - name: Setup Azure CLI
      run: |
        curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
        az extension add --name containerapp --upgrade

    - name: Deploy to Azure Container Apps
      run: |
        chmod +x azContainerApps_deploy.sh
        ./azContainerApps_deploy.sh --deploy-only
      env:
        AZURE_SUBSCRIPTION_ID: \${{ secrets.AZURE_SUBSCRIPTION }}
        AZURE_RESOURCE_GROUP: \${{ secrets.AZURE_RESOURCE_GROUP }}
        AZURE_REGISTRY_URL: \${{ secrets.AZURE_REGISTRY_URL }}
EOF

    echo -e "${GREEN}CI/CD pipeline created${NC}"
    echo -e "${YELLOW}Commit and push to activate the workflow:"
    echo -e "  git add .github/workflows/azure-containerapps-ci.yml"
    echo -e "  git commit -m 'Add CI/CD pipeline'"
    echo -e "  git push origin main${NC}"
}

# Main execution
echo -e "${BLUE}Starting deployment process at $(date)${NC}"
echo -e "Project: ${YELLOW}${PROJECT_PREFIX}${NC}"
echo -e "Environment: ${YELLOW}${ENVIRONMENT_PREFIX}${NC}"
echo -e "Resource Group: ${YELLOW}${PROJECT_RESOURCE_GROUP}${NC}"

# Check dependencies
command -v az >/dev/null 2>&1 || { echo -e "${RED}Azure CLI not installed${NC}"; exit 1; }
command -v gh >/dev/null 2>&1 || { echo -e "${RED}GitHub CLI not installed${NC}"; exit 1; }

# Validate GitHub configuration
validate_github_repo

# Authenticate to GitHub
if ! gh auth status >/dev/null 2>&1; then
    echo -e "${YELLOW}Authenticating to GitHub...${NC}"
    gh auth login
fi

# Create Azure credentials and store in GitHub
create_azure_credentials

# Deploy infrastructure
deploy_infrastructure

# Create CI/CD pipeline
create_cicd_pipeline

echo -e "${GREEN}Deployment completed successfully!${NC}"
echo -e "Log file: ${YELLOW}${log_file}${NC}"