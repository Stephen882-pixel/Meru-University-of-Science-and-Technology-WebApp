from rest_framework import serializers
from .models import APIKey

class APIKeyCreateSerializer(serializers.Serializer):
    #serializer for api key creation request

    developer_id = serializers.CharField(max_length=100,required=True)
    application_name = serializers.CharField(max_length=200,required=True)
    validity_days = serializers.IntegerField(default=365, min_value=1, max_value=3650,required=False)

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
