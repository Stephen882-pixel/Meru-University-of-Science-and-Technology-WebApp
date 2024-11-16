from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'events', views.EventsViewSet, basename='events')

urlpatterns = [
    path('', include(router.urls)),
    path('newsletter/', views.NewsletterSendView.as_view(), name='newsletter'),
    path('subscribe/', views.SubscribeView.as_view(), name='subscribe'),
    path('contact/', views.ContactView.as_view(), name='contact'),
]