"""
URL configuration for MUST project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.messages import api
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from rest_framework.routers import DefaultRouter
from Innovation_WebApp.views import CommunityMembersView, EventRegistrationViewSet,CommunityProfileViewSet,TestimonialViewSet,SessionCreateView,JoinCommunityView

router = DefaultRouter()
router.register(r'event-registrations', EventRegistrationViewSet)

router.register(r'communities', CommunityProfileViewSet)
#router.register(r'community-categories', CommunityCategoryViewSet)
router.register(r'testimonials', TestimonialViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Innovation_WebApp.urls')),
    path('api/',include('Api.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),



    # path('api/',include('Api.urls')),
    # path('accounts/',include('allauth.urls')),
    # path('social/',include('sociallogins.urls')),
    # path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    # path('devs/', include('developers.urls')),




    path('', include(router.urls)),
    path('communities/<int:community_id>/sessions/', SessionCreateView.as_view(), name='create_community_session'),
    path('communities/<int:pk>/members/', CommunityMembersView.as_view(), name='community-members'),
    path('communities/<int:pk>/join/', JoinCommunityView.as_view(), name='join-community'),




]


