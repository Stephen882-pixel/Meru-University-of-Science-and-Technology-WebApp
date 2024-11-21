from django.urls import path
from .views import (
    APIKeyGeneratorView, 
    APIKeyListView, 
    APIKeyDetailView,
    APIKeyDeleteView
)

urlpatterns = [
    path('generate/', APIKeyGeneratorView.as_view(), name='api-key-generate'),
    path('list/', APIKeyListView.as_view(), name='api-key-list'),
    path('<str:prefix>/', APIKeyDetailView.as_view(), name='api-key-detail'),
    path('<str:prefix>/delete/', APIKeyDeleteView.as_view(), name='api-key-delete'),
]
