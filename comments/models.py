from django.db import models
from Innovation_WebApp.models import Events
from django.contrib.auth.models import User

# Create your models here.

class Comment(models.Model):
    post = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} commented on {self.post.title}'