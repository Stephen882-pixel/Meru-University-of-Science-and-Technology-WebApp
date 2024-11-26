from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterSerializer(serializers.Serializer):
    firstname = serializers.CharField(max_length=50)
    lastname = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=50)
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username already exists")
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already exists")
        return data

    def create(self, validated_data):
        user = User.objects.create(
            first_name=validated_data['firstname'],
            last_name=validated_data['lastname'],
            email=validated_data['email'],
            username=validated_data['username'].lower()
        )
        user.set_password(validated_data['password'])
        user.save()  # Don't forget to save the user!
        return validated_data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        # Get user by email
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Account does not exist")
        
        # Check if the credentials are valid
        user = authenticate(username=user.username, password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        
        # Add user to validated data for use in view
        data['user'] = user
        return data

    def get_jwt_token(self, validated_data):
        user = validated_data['user']
        refresh = RefreshToken.for_user(user)

        return {
            'message': 'Login successful',
            'data': {
                'token': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }
            }
        }


