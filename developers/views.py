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

from .utills import TokenService

from rest_framework.exceptions import NotFound
from uuid import UUID
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Developer
from .serializers import DeveloperRegisterSerializer  # Import the serializer

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

        developer = get_object_or_404(Developer, email=email)

        if not check_password(password, developer.password):
            return Response(
                {'error': 'Invalid email or password.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        token = generate_jwt_token(developer)

        return Response(
            {'message': 'Login successful.', 'token': token},
            status=status.HTTP_200_OK
        )



# class APIKeyGeneratorView(APIView):
#     def post(self, request):
#         try:
#             # Extract and validate the JWT token from the Authorization header
#             header = request.headers.get("Authorization")
#             if not header:
#                 return Response(
#                     {"message": "Authorization header is missing"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             try:
#                 token = header.split(' ')[1]
#                 developer_id = get_developer_id_from_token(token)  # Use your token decoding function
#             except IndexError:
#                 return Response(
#                     {"message": "Invalid Authorization header format. Expected 'Bearer <token>'."},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#             except ValueError as e:
#                 return Response(
#                     {"message": f"Invalid token: {str(e)}"},
#                     status=status.HTTP_401_UNAUTHORIZED
#                 )

#             if developer_id is None:
#                 return Response(
#                     {"message": "Invalid or missing developer ID in the token"},
#                     status=status.HTTP_401_UNAUTHORIZED
#                 )

#             # Ensure the developer exists
#             if not Developer.objects.filter(developer_id=developer_id).exists():
#                 return Response(
#                     {"message": "Developer not found"},
#                     status=status.HTTP_404_NOT_FOUND
#                 )

#             # Validate the input data using the serializer
#             serializer = APIKeyCreateSerializer(data=request.data)
#             if not serializer.is_valid():
#                 return Response(
#                     serializer.errors,
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             # Extract validated data
#             application_name = serializer.validated_data['application_name']
#             validity_days = serializer.validated_data.get('validity_days', 365)

#             # Check for an existing active API key
#             existing_key = APIKey.objects.filter(
#                 developer_id=developer_id,
#                 application_name=application_name,
#                 is_active=True
#             ).first()

#             if existing_key:
#                 return Response(
#                     {
#                         "message": "An active API key already exists for this developer and application",
#                         "existing_key_prefix": existing_key.prefix
#                     },
#                     status=status.HTTP_409_CONFLICT
#                 )

#             # Generate secure key
#             raw_key = secrets.token_urlsafe(32)
#             prefix = raw_key[:8]
#             key_hash = hashlib.sha256(raw_key.encode()).hexdigest()

#             # Create API Key entry
#             api_key = APIKey.objects.create(
#                 prefix=prefix,
#                 key_hash=key_hash,
#                 developer_id=developer_id,
#                 application_name=application_name,
#                 expires_at=timezone.now() + timedelta(days=validity_days)
#             )

#             # Serialize and respond
#             response_data = APIKeyDetailSerializer(api_key).data
#             response_data['api_key'] = raw_key  # Include the raw key in the response

#             return Response(response_data, status=status.HTTP_201_CREATED)

#         except Exception as e:
#             return Response(
#                 {"message": f"An error occurred: {str(e)}"},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
    
class APIKeyGeneratorView(APIView):
    def post(self, request):
        try:
            # Extract the token
            header = request.headers.get("Authorization")
            if not header:
                return Response(
                    {"message": "Authorization header is missing"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                token = header.split(' ')[1]
            except IndexError:
                return Response(
                    {"message": "Invalid Authorization header format"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Debug the token first
            debug_info = TokenService.debug_token(token)
            if debug_info['missing_claims']:
                return Response({
                    "message": "Token missing required claims",
                    "missing_claims": debug_info['missing_claims']
                }, status=status.HTTP_401_UNAUTHORIZED)

            try:
                validation_result = TokenService.validate_token(token)
                developer_id = validation_result['payload'].get('developer_id')
            except ValueError as e:
                return Response(
                    {"message": str(e)},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Continue with your existing logic...

            if not developer_id:
                return Response(
                    {"message": "Developer ID not found in token"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

        
            if not Developer.objects.filter(developer_id=developer_id).exists():
                return Response(
                    {"message": "Developer not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Validate the input data using the serializer
            serializer = APIKeyCreateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Extract validated data
            application_name = serializer.validated_data['application_name']
            validity_days = serializer.validated_data.get('validity_days', 365)

            # Check for an existing active API key
            existing_key = APIKey.objects.filter(
                developer_id=developer_id,
                application_name=application_name,
                is_active=True
            ).first()

            if existing_key:
                return Response(
                    {
                        "message": "An active API key already exists for this developer and application",
                        "existing_key_prefix": existing_key.prefix
                    },
                    status=status.HTTP_409_CONFLICT
                )

            # Generate secure key
            raw_key = secrets.token_urlsafe(32)
            prefix = raw_key[:8]
            key_hash = hashlib.sha256(raw_key.encode()).hexdigest()

            # Create API Key entry
            api_key = APIKey.objects.create(
                prefix=prefix,
                key_hash=key_hash,
                developer_id=developer_id,
                application_name=application_name,
                expires_at=timezone.now() + timedelta(days=validity_days)
            )

            # Serialize and respond
            response_data = APIKeyDetailSerializer(api_key).data
            response_data['api_key'] = raw_key  # Include the raw key in the response

            return Response(response_data, status=status.HTTP_201_CREATED)


        except Exception as e:
            return Response(
                {"message": f"An error occurred: {str(e)}"},
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
    """
    View to delete or deactivate a specific API Key
    """
    def delete(self, request, prefix):
        """
        Soft delete (deactivate) an API key
        
        Args:
            request: Django REST framework request object
            prefix: Prefix of the API key to deactivate
        
        Returns:
            Response indicating success or failure
        """
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
