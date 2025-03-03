import re
from venv import logger
from rest_framework import serializers,status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.serializers import ValidationError
import logging
from.models import UserProfile



User = get_user_model()
logger = logging.getLogger(__name__)


class RegisterSerializer(serializers.Serializer):
    firstname = serializers.CharField(max_length=50)
    lastname = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=50)
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)
    #registration_no = serializers.CharField(max_length=50)
    course = serializers.CharField(max_length=50)

    def validate_username(self, value):
        # Additional username validation
        if not re.match(r'^[\w.@+-]+$', value):
            raise serializers.ValidationError("Invalid username format")
        return value

    def validate_password(self, value):
        # Password strength validation
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter")
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("Password must contain at least one number")
        return value
    
    def validate_course(self,value):
        if value.isspace():
            raise serializers.ValidationError("Please provide your course")
        
        return value

    def validate(self, data):
        # Check for existing username and email
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "Username already exists"})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Email already exists"})
        return data
    
        
    

    def create(self, validated_data):
        # Extract user profile
        #registration_no = validated_data.pop('registration_no')
        course = validated_data.pop('course')

        # Create User with 'is_active=False'
        user = User.objects.create_user(
            username=validated_data['username'].lower(),
            email=validated_data['email'],
            first_name=validated_data['firstname'],
            last_name=validated_data['lastname'],
            password=validated_data['password'],
            is_active=True, #User will remain inactive unttil the email is verified 
        )
        UserProfile.objects.create(
            user=user,
            #registration_no=registration_no,
            course=course
        )
        return user
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
        # Exact email match first
             user = User.objects.get(email=email)
        
        # Use Django's default authentication
             if not user.check_password(password):
                  raise serializers.ValidationError("Invalid credentials")

             if not user.is_active:
                  raise serializers.ValidationError("Account is disabled")

             data['user'] = user
             return data

        except User.DoesNotExist:
         raise serializers.ValidationError("Invalid credentials")
    

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate_new_password(self, value):
        """
        Validate password strength requirements
        """
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter")
            
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter")
            
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one number")
            
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Password must contain at least one special character")
            
        return value

    def validate(self, data):
        user = self.context['request'].user
        
        # Verify user is authenticated
        if not user.is_authenticated:
            raise serializers.ValidationError({
                "detail": "Authentication required"
            })

        # Check if old password is correct
        if not user.check_password(data['old_password']):
            raise serializers.ValidationError({
                "old_password": "Current password is incorrect"
            })

        # Confirm new passwords match
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({
                "confirm_password": "New passwords do not match"
            })

        # Ensure new password is different from old password
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError({
                "new_password": "New password must be different from current password"
            })

        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user




