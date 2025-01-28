# serializers.py
from rest_framework import serializers
from .models import NormalUser
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterSerializer(serializers.Serializer):
    firstname = serializers.CharField(max_length=50)
    lastname = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=50)
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        if NormalUser.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username already exists")
        if NormalUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already exists")
        return data

    def create(self, validated_data):
        user = NormalUser(
            first_name=validated_data['firstname'],
            last_name=validated_data['lastname'],
            email=validated_data['email'],
            username=validated_data['username'].lower()
        )
        user.set_password(validated_data['password'])
        user.save()
        return validated_data

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        try:
            user = NormalUser.objects.get(email=data['email'])
        except NormalUser.DoesNotExist:
            raise serializers.ValidationError("Account does not exist")

        if not user.check_password(data['password']):
            raise serializers.ValidationError("Invalid credentials")

        data['user'] = user
        return data

    def get_jwt_token(self, validated_data):
        user = validated_data['user']
        # Create custom claims for JWT token
        refresh = RefreshToken()
        refresh['user_id'] = str(user.user_id)
        refresh['email'] = user.email
        refresh['username'] = user.username
        refresh['type'] = 'normal_user'  # To distinguish from developer tokens

        return {
            'message': 'Login successful',
            'data': {
                'token': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }
            }
        }
    
class NormalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NormalUser
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name']  # Add fields you want to expose
