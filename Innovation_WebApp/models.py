from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField
import uuid
from django.core.validators import EmailValidator

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
    

class EventRegistration(models.Model):
    AGE_BRACKETS = [
        ('16-18', '16-18'),
        ('19-21', '19-21'),
        ('22-24', '22-24'),
        ('25+', '25 and above')
    ]

    EDUCATION_LEVELS = [
    ('year_1', 'Year 1'),
    ('year_2', 'Year 2'),
    ('year_3', 'Year 3'),
    ('year_4', 'Year 4'),
    ('postgraduate', 'Postgraduate')
    ]
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey('Events', on_delete=models.CASCADE, related_name='registrations')
    full_name = models.CharField(max_length=200)
    email = models.EmailField(validators=[EmailValidator()])
    age_bracket = models.CharField(max_length=20, choices=AGE_BRACKETS)
    #year_of_study = models.CharField(max_length=50)
    course = models.CharField(max_length=200)
    educational_level = models.CharField(max_length=20, choices=EDUCATION_LEVELS)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    registration_timestamp = models.DateTimeField(auto_now_add=True)
    ticket_number = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return f"{self.full_name} - {self.event.name}"

