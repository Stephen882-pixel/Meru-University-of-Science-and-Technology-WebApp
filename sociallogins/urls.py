from django.urls import path,include
from django.contrib import admin
from .views import home,logout_view

urlpatterns = [
    path('login/',home),
    path('logout/',logout_view),
    path('accounts/', include('allauth.urls')),
]