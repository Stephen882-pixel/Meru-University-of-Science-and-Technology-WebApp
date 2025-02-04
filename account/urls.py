from django.urls import path
from django.contrib import admin
from account.views import ChangePasswordView, CustomTokenRefreshView, LogoutView, PasswordResetConfirmView, PasswordResetView, RegisterView,LoginView, UserDataView,VerifyEmailView,EmailVerificationView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    # Authentication Routes
    path('register/',RegisterView.as_view(),name='register'),
    #path('verify-email/',VerifyEmailView.as_view,name='verify_email'),
    path('verify-email/<str:token>', EmailVerificationView.as_view(), name='verify_email'),
    path('login/',LoginView.as_view(),name='login'),

    # Authentication Routes
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),

    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # JWT Token Routes
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    #path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    

    # get user data with access tokens
    path('get-user-data/',UserDataView.as_view(),name='get_user_data')


   
]