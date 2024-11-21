from django.urls import path
from .views import (
    APIKeyGeneratorView, 
    APIKeyListView, 
    APIKeyDetailView,
    APIKeyDeleteView,
    DeveloperRegisterView,
    DeveloperLoginView
)
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register', DeveloperRegisterView.as_view(), name='developer-register'),
    path('login', DeveloperLoginView.as_view(), name='developer-login'),
    path('token/refresh', TokenRefreshView.as_view(), name='token-refresh'),
    path('generate', APIKeyGeneratorView.as_view(), name='api-key-generate'),
    path('list/', APIKeyListView.as_view(), name='api-key-list'),
    path('<str:prefix>', APIKeyDetailView.as_view(), name='api-key-detail'),
    path('<str:prefix>/delete', APIKeyDeleteView.as_view(), name='api-key-delete'),
]


