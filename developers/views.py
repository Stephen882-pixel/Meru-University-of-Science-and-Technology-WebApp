from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
import secrets
import hashlib
from .models import APIKey
from .serializers import APIKeyCreateSerializer,APIKeyDetailSerializer

# Create your views here.

class APIKeyGeneratorView(APIView):
    def post(self, request):
        serializer = APIKeyCreateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Extract validated data
        developer_id = serializer.validated_data['developer_id']
        application_name = serializer.validated_data['application_name']
        validity_days = serializer.validated_data.get('validity_days', 365)
        
        try:
            # Check for existing active API key for this developer and application
            existing_key = APIKey.objects.filter(
                developer_id=developer_id, 
                application_name=application_name,
                is_active=True
            ).first()
            
            if existing_key:
                return Response(
                    {
                        'error': 'An active API key already exists for this developer and application',
                        'existing_key_prefix': existing_key.prefix
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
            
            # Prepare response
            response_data = {
                'api_key': raw_key,
                'details': APIKeyDetailSerializer(api_key).data
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response(
                {'error': str(e)}, 
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
