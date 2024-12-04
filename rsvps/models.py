from django.db import models
from Innovation_WebApp.models import Events

# Create your models here.
class RSVP(models.Model):
    event = models.ForeignKey(Events, related_name='rsvps', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    attending = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


