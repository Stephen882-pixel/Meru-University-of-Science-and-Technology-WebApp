from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
import secrets
import hashlib
from .models import APIKey,Developer
from .serializers import APIKeyCreateSerializer,APIKeyDetailSerializer,DeveloperRegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from .utils import generate_jwt_token,get_developer_id_from_token

from rest_framework.exceptions import NotFound
from uuid import UUID
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Developer
from .serializers import DeveloperRegisterSerializer  # Import the serializer
import logging

logger = logging.getLogger(__name__)

class DeveloperRegisterView(APIView):
    def post(self, request):
        # Use the serializer to validate and save the developer data
        serializer = DeveloperRegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            developer = serializer.save()  # This calls the create method in the serializer

            # Serialize the developer object to return a JSON response
            return Response(
                {'message': 'Developer registered successfully.', 'user': serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )



class DeveloperLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {'error': 'Email and password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            developer = Developer.objects.get(email=email)
        except Developer.DoesNotExist:
            return Response(
                {'error': 'Invalid email or password.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not check_password(password, developer.password):
            return Response(
                {'error': 'Invalid email or password.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        token = generate_jwt_token(developer)

        return Response({
            'access': str(token),
            'token_type': 'Bearer'
        }, status=status.HTTP_200_OK)



    
class APIKeyGeneratorView(APIView):
    def post(self, request):
        try:
            # Extract and validate the JWT token
            header = request.headers.get("Authorization")
            if not header:
                return Response(
                    {"error": "Authorization header is missing"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            try:
                token = header.split(' ')[1]
                developer_id = get_developer_id_from_token(token)  # Extract developer_id
            except IndexError:
                return Response(
                    {"error": "Invalid Authorization header format. Expected 'Bearer <token>'"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            except ValueError as e:
                return Response(
                    {"error": f"Invalid token: {str(e)}"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Validate request data
            serializer = APIKeyCreateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {"error": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Extract validated data
            application_name = serializer.validated_data['application_name']
            validity_days = serializer.validated_data.get('validity_days', 365)
            rate_limit = serializer.validated_data.get('rate_limit', 1000)

            # Check for existing active key
            existing_key = APIKey.objects.filter(
                api_key_id=developer_id,
                application_name=application_name,
                is_active=True
            ).first()

            if existing_key:
                return Response({
                    "error": "An active API key already exists for this application",
                    "existing_key_prefix": existing_key.prefix,
                    "application_name": existing_key.application_name
                }, status=status.HTTP_409_CONFLICT)

            # Generate secure key
            raw_key = secrets.token_urlsafe(32)
            prefix = raw_key[:8]
            key_hash = hashlib.sha256(raw_key.encode()).hexdigest()

            # Calculate expiration date
            expires_at = timezone.now() + timedelta(days=validity_days)

            try:
                # Create API Key entry
                api_key = APIKey.objects.create(
                    api_key_id=developer_id,  # Use developer_id as api_key_id
                    prefix=prefix,
                    key_hash=key_hash,
                    application_name=application_name,
                    expires_at=expires_at,
                    rate_limit=rate_limit
                )
            except Exception as e:
                logger.error(f"Failed to create API key: {str(e)}")
                return Response(
                    {"error": "Failed to generate API key. Please try again."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Prepare response
            response_data = APIKeyDetailSerializer(api_key).data
            response_data.update({
                'api_key': raw_key,  # Only time the raw key is shown
                'message': 'API key generated successfully. Please store it securely - you won\'t be able to see it again.'
            })
            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"API key generation failed: {str(e)}", exc_info=True)
            return Response(
                {"error": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class APIKeyListView(APIView):
    """
    View to list all API Keys
    """
    def get(self, request):
        """
        Retrieve all API Keys
        """
        api_keys = APIKey.objects.all()
        serializer = APIKeyDetailSerializer(api_keys, many=True)
        return Response(serializer.data)

##getting specific  api_key   

class APIKeyDetailView(APIView):
    """
    View to retrieve details of a specific API Key
    """
    def get(self, request, prefix):
        
        try:
            # Retrieve the API key or return 404
            api_key = get_object_or_404(APIKey, prefix=prefix)
            
            # Serialize and return the key details
            serializer = APIKeyDetailSerializer(api_key)
            return Response(serializer.data)
        
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class APIKeyDeleteView(APIView):
   
    def delete(self, request, prefix):
        
        
        try:
            # Retrieve the API key or return 404
            api_key = get_object_or_404(APIKey, prefix=prefix)
            
            # Soft delete by marking as inactive
            api_key.is_active = False
            api_key.save()
            
            return Response(
                {'message': f'API Key {prefix} has been deactivated'}, 
                status=status.HTTP_200_OK
            )
        
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
