from django.urls import path,include
from django.contrib import admin
from .views import home,logout_view,social_login_callback,api_logout

urlpatterns = [
    # path('login/',home),
    path('logout/',logout_view),
    path('accounts/', include('allauth.urls')),
    path('accounts/mobile-callback/',social_login_callback, name='mobile_callback'),
    path('api/logout/', api_logout, name='api_logout'),
]