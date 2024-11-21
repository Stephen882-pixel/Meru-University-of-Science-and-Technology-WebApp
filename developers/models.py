from django.db import models
from django.utils import timezone
import secrets
import hashlib

# Create your models here.

class APIKey(models.Model):
    prefix = models.CharField(max_length=8, unique=True)
    key_hash = models.CharField(max_length=64, unique=True)
    developer_id = models.CharField(max_length=100)
    application_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    rate_limit = models.IntegerField(default=1000)
    
    class Meta:
        # Add a unique constraint for active keys
        unique_together = [
            ['developer_id', 'application_name']
        ]
        
        # Optional index to improve query performance
        indexes = [
            models.Index(fields=['developer_id', 'application_name'])
        ]
    
    def __str__(self):
        return f"{self.application_name} - {self.prefix}"
