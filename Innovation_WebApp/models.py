from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField
from django.conf import settings

class SubscribedUsers(models.Model):
    email = models.EmailField(unique=True, max_length=100)
    created_date = models.DateTimeField('Date created', default=timezone.now)

    def __str__(self):
        return self.email


class Events(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.URLField(default="event_images/default.png")  # S3 image URL will be stored here
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    organizer = models.CharField(max_length=100)
    contact_email = models.EmailField(null=True, blank=True)
    is_virtual = models.BooleanField(default=False)
    registration_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    Post = models.ForeignKey(Events,on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"

    

