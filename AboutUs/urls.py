from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import ClubViewSet,CommunityViewSet,ExecutiveMemberViewSet,SocialMediaViewSet


router = DefaultRouter()
router.register(r'clubs',ClubViewSet)
router.register(r'communities',CommunityViewSet)
router.register(r'executives',ExecutiveMemberViewSet)
router.register(r'social-media',SocialMediaViewSet)


urlpatterns = [
    path('', include(router.urls))
]
