from requests import Session
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

# class EventsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Events
#         fields = ['id', 'name', 'title', 'description', 'image', 'date', 'location', 'organizer', 'contact_email', 'is_virtual', 'registration_link']


#this one has s3 bucket funcionality
# class EventsSerializer(serializers.ModelSerializer):
#     image_field = serializers.ImageField(write_only=True, required=False)

#     class Meta:
#         model = Events
#         fields = '__all__'
#         extra_kwargs = {
#             'image': {'read_only': True}  # The `image` field will be read-only, URL is auto-filled.
#         }

#     def update(self, instance, validated_data):
#         # Extract the `image_field` data from the request
#         image_file = validated_data.pop('image', None)

#         if image_file:
#             # Initialize the S3 client
#             s3_client = boto3.client(
#                 's3',
#                 aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#                 aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
#             )

#             # Generate a unique file name
#             filename = f"events/{uuid.uuid4()}_{image_file.name}"

#             # Upload the file to the S3 bucket
#             s3_client.upload_fileobj(
#                 image_file,
#                 settings.AWS_STORAGE_BUCKET_NAME,
#                 filename,
#                 ExtraArgs={'ContentType': image_file.content_type}  # Ensure correct content type
#             )

#             # Generate the public URL for the uploaded image
#             instance.image = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{filename}"

#         # Update other fields and save the instance
#         return super().update(instance, validated_data)


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
        read_only_fields = ['uid', 'registration_timestamp', 'ticket_number']

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
            'id', 'name','community_lead', 'co_lead', 
            'treasurer', 'secretary', 'email', 'phone_number', 
            'github_link', 'linkedin_link', 'description', 
            'founding_date', 'total_members', 'is_recruiting', 
            'tech_stack', 'sessions','members'
        ]

    def get_total_members(self, obj):
        # Dynamically calculate total number of members related to the community
        return obj.members.count()

    def create(self, validated_data):
        sessions_data = validated_data.pop('sessions',[])
        members_data = validated_data.pop('members', []) 
        community = CommunityProfile.objects.create(**validated_data)
        for session_data in sessions_data:
            Session.objects.create(community=community, **session_data)
        return community

    def update(self, instance, validated_data):
        sessions_data = validated_data.pop('sessions', [])
        members_data = validated_data.pop('members', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update sessions
        instance.sessions.all().delete()  # Clear existing sessions
        for session_data in sessions_data:
            Session.objects.create(community=instance, **session_data)
        
        instance.members.all().delete()  # Delete existing members
        for member_data in members_data:
            CommunityMember.objects.create(community=instance, **member_data)

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