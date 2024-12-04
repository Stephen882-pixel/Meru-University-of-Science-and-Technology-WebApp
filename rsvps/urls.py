from django.urls import path
from .views import RSVPCreateView

urlpatterns = [
    path('create/', RSVPCreateView.as_view(), name='rsvp-create'),
]