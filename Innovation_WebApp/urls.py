from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'events', views.EventViewSet, basename='events')

urlpatterns = [
    path('', include(router.urls)),
    path('newsletter/', views.NewsletterSendView.as_view(), name='newsletter'),
    path('subscribe/', views.SubscribeView.as_view(), name='subscribe'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('comments/create/', views.CommentCreateView.as_view(), name='comment-create'),
    path('comments/update/', views.CommentUpdateView.as_view(), name='comment-update'),
    path('comments/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),
    path('comments/all/', views.CommentListView.as_view(), name='comment-all'),
]