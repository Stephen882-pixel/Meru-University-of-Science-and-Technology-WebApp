from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField

class SubscribedUsers(models.Model):
    email = models.EmailField(unique=True, max_length=100)
    created_date = models.DateTimeField('Date created', default=timezone.now)

    def __str__(self):
        return self.email

class Events(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField()
    # image = models.TextField(upload_to='uploads/event/', null=True, blank=True)
    image = models.TextField(null=True, blank=True)
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    organizer = models.CharField(max_length=100)
    contact_email = models.EmailField(null=True, blank=True)
    is_virtual = models.BooleanField(default=False)
    registration_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title