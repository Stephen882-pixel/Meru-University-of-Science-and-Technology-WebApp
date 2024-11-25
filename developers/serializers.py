from rest_framework import serializers
from .models import APIKey,Developer
from django.core.validators import MinValueValidator, MaxValueValidator


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


class APIKeyCreateSerializer(serializers.Serializer):
    application_name = serializers.CharField(
        max_length=200,
        required=True
    )
    validity_days = serializers.IntegerField(
        required=False,
        default=365,
        min_value=1,
        max_value=730
    )
    rate_limit = serializers.IntegerField(
        required=False,
        default=1000,
        min_value=1,
        max_value=10000
    )

class APIKeyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKey
        fields = [
            'prefix',
            'api_key_id',  # Changed to api_key_id
            'application_name',
            'created_at',
            'expires_at',
            'is_active',
            'rate_limit'
        ]
