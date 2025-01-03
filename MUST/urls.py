from django.contrib import admin
from django.contrib.messages import api
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Innovation_WebApp.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/',include('Api.urls')),
    path('accounts/',include('allauth.urls')),
    path('social/',include('sociallogins.urls')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('devs/', include('developers.urls')),
    path('rsvps/', include('rsvps.urls')),
    path('users/', include('account.urls')),
]


