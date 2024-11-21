from rest_framework import serializers
from .models import APIKey,Developer


class DeveloperRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    developer_id = serializers.UUIDField(read_only=True)  # Include developer_id as read-only

    class Meta:
        model = Developer
        fields = ['developer_id', 'username', 'email', 'password']

    def create(self, validated_data):
        # Use the create_user method which handles password hashing
        return Developer.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )




class APIKeyCreateSerializer(serializers.ModelSerializer):
    application_name = serializers.CharField(required=True, max_length=255)  
    validity_days = serializers.IntegerField(required=False, min_value=1)  

    class Meta:
        model = APIKey
        fields = ['application_name', 'validity_days'] 


class APIKeyDetailSerializer(serializers.ModelSerializer):
    # serializer for API key response
    
    class Meta:
        model = APIKey
        fields = [
            'prefix',
            'developer_id',
            'application_name',
            'created_at',
            'expires_at',
            'is_active',
            'rate_limit'
        ]
        read_only_fields = fields 
