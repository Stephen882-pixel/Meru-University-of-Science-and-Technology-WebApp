from rest_framework import serializers
from .models import SubscribedUsers, Events

class SubscribedUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscribedUsers
        fields = ['id', 'email', 'created_date']

class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ['id', 'name', 'title', 'description', 'image', 'date', 'location', 'organizer', 'contact_email', 'is_virtual', 'registration_link']