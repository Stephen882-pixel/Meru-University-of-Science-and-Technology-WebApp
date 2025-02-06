from grpc import Status
from requests import Response, Session
from rest_framework import serializers

from Innovation_WebApp.Email import send_ticket_email
from .models import CommunityMember, SubscribedUsers, Events,EventRegistration,CommunityProfile,CommunitySession,Testimonial
import boto3
from django.conf import settings
import uuid

from .utils import send_ticket_email


class SubscribedUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscribedUsers
        fields = ['id', 'email', 'created_date']


class EventsSerializer(serializers.ModelSerializer):
    image_field = serializers.ImageField(write_only=True, required=False)  # To handle image upload

    class Meta:
        model = Events
        fields = '__all__'
        extra_kwargs = {
            'image': {'read_only': True}  # This field will store the S3 URL and is read-only
        }

    def create(self, validated_data):
        # Extract `image_field` from the validated data
        image_file = validated_data.pop('image_field', None)

        # Create the event instance
        event_instance = Events.objects.create(**validated_data)

        # Handle S3 upload if an image is provided
        if image_file:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )

            # Generate a unique file name
            filename = f"event_images/{uuid.uuid4()}_{image_file.name}"

            # Upload the file to S3
            s3_client.upload_fileobj(
                image_file,
                settings.AWS_STORAGE_BUCKET_NAME,
                filename,
                ExtraArgs={'ContentType': image_file.content_type}
            )

            # Set the public S3 URL in the `image` field
            event_instance.image = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{filename}"
            event_instance.save()

        return event_instance
        
   

    def update(self, instance, validated_data):
        # Extract `image_field` from the validated data
        image_file = validated_data.pop('image_field', None)

        # Update the instance fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Handle S3 upload if an image is provided
        if image_file:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )

            # Generate a unique file name
            filename = f"event_images/{uuid.uuid4()}_{image_file.name}"

            # Upload the file to S3
            s3_client.upload_fileobj(
                image_file,
                settings.AWS_STORAGE_BUCKET_NAME,
                filename,
                ExtraArgs={'ContentType': image_file.content_type}
            )

            # Update the public S3 URL in the `image` field
            instance.image = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{filename}"

        instance.save()
        return instance
    

class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = '__all__'
        #exclude = ('uid',)
        read_only_fields = [ 'registration_timestamp', 'ticket_number']

    def create(self, validated_data):
        registration = super().create(validated_data)
        
        # Send ticket email
        send_ticket_email(registration)
        
        return registration
    
class CommunitySessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunitySession
        fields = ['day', 'start_time', 'end_time', 'meeting_type', 'location']

class CommunityMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityMember
        fields = ['id', 'name', 'email', 'joined_at']

class CommunityProfileSerializer(serializers.ModelSerializer):
    sessions = CommunitySessionSerializer(many=True, read_only=True)
    members = CommunityMemberSerializer(many=True, read_only=True)
    
    class Meta:
        model = CommunityProfile
        fields = [
            'id', 'name', 'community_lead', 'co_lead', 
            'secretary', 'email', 'phone_number', 
            'github_link', 'linkedin_link', 'description', 
            'founding_date',  'is_recruiting', 
            'tech_stack','members','total_members','sessions'
        ]

    def create(self, validated_data):
        sessions_data = validated_data.pop('sessions', [])
        members_data = validated_data.pop('members', []) 
        community = CommunityProfile.objects.create(**validated_data)
        
        # Create sessions
        for session_data in sessions_data:
            Session.objects.create(community=community, **session_data)
        
        #Create members
        for member_data in members_data:
            CommunityMember.objects.create(community=community, **member_data)
        
        #Update total members
        community.update_total_members()
        
        return community

    def update(self, instance, validated_data):
        sessions_data = validated_data.pop('sessions', [])
        members_data = validated_data.pop('members', [])
        
        # Update community profile attributes
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update sessions
        instance.sessions.all().delete()
        for session_data in sessions_data:
            Session.objects.create(community=instance, **session_data)
        
        # Update members
        instance.members.all().delete()
        for member_data in members_data:
            CommunityMember.objects.create(community=instance, **member_data)
        
        # Update total members
        instance.update_total_members()
        
        return instance

class TestimonialSerializer(serializers.ModelSerializer):
    #author_username = serializers.ReadOnlyField(source='author.username')
    
    class Meta:
        model = Testimonial
        # fields = [
        #     'id', 'author_username', 'community', 
        #     'content', 'rating', 'created_at'
        # ]
        # read_only_fields = ['author', 'created_at']

# class CommunityCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CommunityCategory
#         fields = ['id', 'name', 'description']




class CommunityJoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityMember
        fields = ['community', 'name', 'email']