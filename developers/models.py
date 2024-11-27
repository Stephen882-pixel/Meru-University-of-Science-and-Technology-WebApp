from django.db import models

# Create your models here.
from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.contrib.auth import get_user_model
import secrets
import hashlib

# Create your models here.


class DeveloperManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("The Email field is required")
        if not username:
            raise ValueError("The Username field is required")
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Developer(AbstractBaseUser):
    developer_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True,primary_key=True)  # Auto-generated UUID
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = DeveloperManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f"{self.username} ({self.developer_id})"





class APIKey(models.Model):
    api_key_id = models.UUIDField()  # This will store the developer_id from the token
    prefix = models.CharField(max_length=8, unique=True)
    key_hash = models.CharField(max_length=64, unique=True)
    application_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    rate_limit = models.IntegerField(default=1000)

    class Meta:
        unique_together = [['api_key_id', 'application_name']]
        indexes = [
            models.Index(fields=['api_key_id', 'application_name'])
        ]

    def __str__(self):
        return f"{self.application_name} - {self.prefix}"
