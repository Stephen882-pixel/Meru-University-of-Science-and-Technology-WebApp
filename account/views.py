from venv import logger
import logging
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response

from account.models import PasswordResetRequest
from .serializers import RegisterSerializer, LoginSerializer,ChangePasswordSerializer,status
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from account import serializers


import secrets
from django.core.mail import send_mail
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from.models import UserProfile


# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            user_profile = UserProfile.objects.get(user=user)
            user_data = {
                'username':str(user.username),
                'email':str(user.email),
                'first_name':str(user.first_name),
                'last_name':str(user.last_name),
                'registration_no':str(user_profile.registration_no),
                'course':str(user_profile.course)
            }
            return Response({
                'message': 'Account created successfully',
                'user_data':user_data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = []
    authentication_classes = []
    
    def post(self, request):
        try:
            serializer = LoginSerializer(
                data=request.data, 
                context={'request': request}
            )
            
            serializer.is_valid(raise_exception=True)

            user = serializer.validated_data['user']
            tokens = self.get_tokens_for_user(user)
            
            return Response({
                'status': 'success',
                'tokens': tokens,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'Login processing failed: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(
                data=request.data,
                context={'request': request}
            )

            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'success',
                    'message': 'Password changed successfully'
                }, status=status.HTTP_200_OK)

            return Response({
                'status': 'error',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'An unexpected error occurred',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class PasswordResetView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            
            # Generate unique reset token
            token = secrets.token_urlsafe(32)
            
            # Create password reset request
            reset_request = PasswordResetRequest.objects.create(
                user=user, 
                token=token
            )
            
            # Construct reset link
            reset_url = f"{settings.FRONTEND_URL}/reset-password/{token}"
            
            # Send reset email
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_url}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            return Response({
                'message': 'Password reset link sent to your email'
            }, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({
                'error': 'No user found with this email'
            }, status=status.HTTP_404_NOT_FOUND)

class PasswordResetConfirmView(APIView):
    def post(self, request):
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        
        try:
            reset_request = PasswordResetRequest.objects.get(
                token=token, 
                is_used=False,
                created_at__gt=timezone.now() - timezone.timedelta(hours=1)
            )
            
            user = reset_request.user
            user.set_password(new_password)
            user.save()
            
            # Mark token as used
            reset_request.is_used = True
            reset_request.save()
            
            return Response({
                'message': 'Password reset successful'
            }, status=status.HTTP_200_OK)
        
        except PasswordResetRequest.DoesNotExist:
            return Response({
                'error': 'Invalid or expired reset token'
            }, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Blacklist refresh token
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response({
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'message': 'Invalid token'
            }, status=status.HTTP_400_BAD_REQUEST)
        

class UserDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        # Get the authenticated user
        user = request.user
        try:
            # fetch user profile details
            user_profile = UserProfile.objects.get(user=user)

            # Return user data
            user_data = {
                'username':user.username,
                'email':user.email,
                'first_name':user.first_name,
                'last_name':user.last_name,
                'registration_no':user_profile.registration_no,
                'course':user_profile.course
            }
            return Response({
                'message':'User data retrieved successfully',
                'user_data':user_data
            },status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({
                'error':'User profile does not exist'
            },status=status.HTTP_404_NOT_FOUND)

# google oauth 
