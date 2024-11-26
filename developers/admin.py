from django.contrib import admin

# Register your models here.
# admin.py
from django.contrib import admin
from .models import Developer, APIKey

# Register the Developer model
@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ('developer_id', 'username', 'email', 'date_joined', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    ordering = ('date_joined',)

# Register the APIKey model
@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('api_key_id', 'prefix', 'application_name', 'created_at', 'expires_at', 'is_active')
    search_fields = ('application_name', 'prefix')
    list_filter = ('is_active', 'expires_at')
    ordering = ('created_at',)
