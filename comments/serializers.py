from rest_framework import serializers
from .models import Comment
from django.contrib.auth.models import User

class CommentSerializer(serializers.ModelSerializer):
    post = serializers.IntegerField(write_only=True)
  # For creating comments
    user = serializers.UUIDField(write_only=True)  # Use UUIDField for user_id
    id = serializers.IntegerField(write_only=True)  # Use UUIDField for user_id
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'text', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CommentUpdateSerializer(serializers.ModelSerializer):
    user = serializers.UUIDField(write_only=True)
    id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_user(self, value):
        try:
            # Convert UUID to NormalUser instance
            return User.objects.get(user_id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")