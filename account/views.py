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
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework.exceptions import ValidationError


# Create your views here.
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings


import jwt
from rest_framework import status
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenRefreshView
import traceback
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()

            # Call the email verification function without passing `request`
            try:
                self.send_verification_email(user)
            except Exception as e:
                return Response({
                    "message": f"Failed to send verification email: {str(e)}"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            user_profile = UserProfile.objects.get(user=user)
            user_data = {
                'username': str(user.username),
                'email': str(user.email),
                'first_name': str(user.first_name),
                'last_name': str(user.last_name),
                #'registration_no': str(user_profile.registration_no),
                'course': str(user_profile.course)
            }
            return Response({
                'message': 'Account created successfully. Please check your email for verification instructions.',
                'status':'success',
                'user_data': None
            }, status=status.HTTP_201_CREATED)

        return Response({
            'message':'There was a problem signing up.Please try again',
            'status': serializer.errors,
            'data':None
        }, status=status.HTTP_400_BAD_REQUEST)

    def send_verification_email(self, user):
        token = self.generate_verification_token(user)
        verification_url = f"{settings.FRONTEND_BASE_URL}/verify-email/{token}"

        send_mail(
            subject="Email Verification",
            message=f"Please verify your email by clicking this link: {verification_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

    def generate_verification_token(self, user):
        """Generates a JWT token for email verification."""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

# Helper function for sending email verification
def send_verification_email(user):
    token = generate_verification_token(user)

    verification_url = f"{settings.FRONTEND_BASE_URL}/verify-email/{token}"

    send_mail(
        subject="Email Verification",
        message=f"Please verify your email by clicking this link: {verification_url}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

def generate_verification_token(user):
    """Generates a JWT token for email verification."""
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)



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
            # check if the user is verified
            if not user.is_active:
                return Response({
                    'message':'Email not verified.Please verify your email.',
                    'status':'error',
                    'data':None
                },status=status.HTTP_403_FORBIDDEN)
            
            tokens = self.get_tokens_for_user(user)
            
            return Response({
                'message':'Login successfull',
                'status': 'success',
                'data':tokens
                
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'message': f'Login processing failed',
                'status': serializer.errors,
                'data':None
            }, status=status.HTTP_403_FORBIDDEN)

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
                    'message': 'Password changed successfully',
                    'status': 'success',
                    'data':None
                }, status=status.HTTP_200_OK)

            return Response({
                'message':'An error occured.Please try again',
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
                'id':user.id,
                'username':user.username,
                'email':user.email,
                'first_name':user.first_name,
                'last_name':user.last_name,
                #'registration_no':user_profile.registration_no,
                'course':user_profile.course
            }
            return Response({
                'message':'User data retrieved successfully',
                'status':'success',
                'data':user_data
            },status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({
                'error':'User profile does not exist'
            },status=status.HTTP_404_NOT_FOUND)
        
def send_verification_email(self, user):
    token = self.generate_verification_token(user)
    verification_url = f"{settings.FRONTEND_BASE_URL}/{token}"



    send_mail(
        subject="Email Verification",
        message=f"Please verify your email by clicking this link: {verification_url}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

class VerifyEmailView(APIView):
    def get(self,request):
        uid =request.GET.get('uid')
        token = request.GET.get('token')

        try:
            # Decode user ID
            user_id = urlsafe_base64_encode(uid).decode()
            user = User.objects.get(pk=user_id)

            # Check token validity
            if default_token_generator.check_token(user,token):
                user.is_active = True
                user.save()
                return Response({
                    'message':'Emale verified successfully.You can now login'
                },status=status.HTTP_200_OK)
            else:
                return Response({
                    'message':'Invalide or expired Token'
                },status=status.HTTP_400_BAD_REQUEST)
        except (User.DoesNotExist,ValueError,TypeError):
            return Response({
                'message':'Invalide token or user ID'
            },status=status.HTTP_400_BAD_REQUEST)
        
class EmailVerificationView(APIView):
    def get(self,request,token):
        try:
            # Decode the token (you can replace this with your actual token validation)
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])

            # Mark user as active
            user.is_active =  True
            user.save()


            return HttpResponse("Email verified successfully!", status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return HttpResponse("Verification token has expired", status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidTokenError:
            return HttpResponse("Invalid token", status=status.HTTP_400_BAD_REQUEST)

class CustomTokenRefreshView(TokenRefreshView):
    def post(self,request,*args,**kwargs):
        try:
            old_refresh_token = RefreshToken(request.data['refresh'])
            user = User.objects.get(id=old_refresh_token['user_id'])
            new_refresh = RefreshToken.for_user(user)
            new_refresh = RefreshToken.for_user(user)
            return Response({
                'message':'User logged in',
                'status':'success',
                'data':{
                    'access':str(new_refresh.access_token),
                    'refresh':str(new_refresh)
                }
            },status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error:{str(e)}")
            print(traceback.format_exc())
            return Response({
                'message':'User not logged in',
                'status':'error',
                'data':None
            },status=status.HTTP_401_UNAUTHORIZED)


# google oauth 
