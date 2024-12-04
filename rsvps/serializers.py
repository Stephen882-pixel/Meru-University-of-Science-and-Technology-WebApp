from rest_framework import serializers
from .models import RSVP
from Innovation_WebApp.models import Events

class RSVPSerializer(serializers.ModelSerializer):
    class Meta:
        model = RSVP
        fields = ['full_name', 'email', 'phone_number', 'attending']

class EventRSVPSerializer(serializers.ModelSerializer):
    rsvps = RSVPSerializer(many=True, read_only=True)

    class Meta:
        model = Events
        fields = ['id', 'rsvps']
