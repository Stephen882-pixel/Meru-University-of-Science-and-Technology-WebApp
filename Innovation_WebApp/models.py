from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField
import uuid
from django.core.validators import EmailValidator,MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

#from django.contrib.auth.models import User

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
    
# class CommunityCategory(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     description = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return self.name
    
class CommunityProfile(models.Model):
    MEETING_TYPES = [
        ('VIRTUAL', 'Virtual'),
        ('PHYSICAL', 'Physical'),
        ('HYBRID', 'Hybrid')
    ]

    name = models.CharField(max_length=200)
    community_lead = models.CharField(max_length=200)
    co_lead = models.CharField(max_length=200, blank=True, null=True)
    treasurer = models.CharField(max_length=200, blank=True, null=True)
    secretary = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    description = models.TextField()
    founding_date = models.DateField(blank=True, null=True)
    total_members = models.IntegerField(default=0)
    is_recruiting = models.BooleanField(default=False)
    tech_stack = models.JSONField(blank=True, null=True)

    def update_total_members(self):
        current_count = self.members.count()
        if self.total_members != current_count:
            CommunityProfile.objects.filter(id=self.id).update(total_members=current_count)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only for new instances
            super().save(*args, **kwargs)
            self.update_total_members()
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_sessions(self):
        return self.sessions.all()
    
    @receiver([post_save, post_delete], sender='Innovation_WebApp.CommunityMember')
    def update_community_member_count(sender, instance, **kwargs):
        if instance.community:
            instance.community.update_total_members()
    
    
class CommunitySession(models.Model):
    DAYS_OF_WEEK = [
        ('MONDAY', 'Monday'),
        ('TUESDAY', 'Tuesday'),
        ('WEDNESDAY', 'Wednesday'),
        ('THURSDAY', 'Thursday'),
        ('FRIDAY', 'Friday'),
        ('SATURDAY', 'Saturday'),
        ('SUNDAY', 'Sunday')
    ]

    community = models.ForeignKey(CommunityProfile, related_name='sessions', on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    meeting_type = models.CharField(max_length=10, choices=CommunityProfile.MEETING_TYPES)
    location = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.community.name} - {self.get_day_display()} Session"
    
class Testimonial(models.Model):
    #author = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(CommunityProfile, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Testimonial by {self.author.username}"
    

class CommunityMember(models.Model):
    community = models.ForeignKey(CommunityProfile, related_name='members', on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.community.name})"
    



