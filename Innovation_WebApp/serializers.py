from grpc import Status
from requests import Response, Session
from rest_framework import serializers

from Innovation_WebApp.Email import send_ticket_email
from .models import CommunityMember, SubscribedUsers, Events,EventRegistration,CommunityProfile,CommunitySession,Testimonial
import boto3
from django.conf import settings
import uuid
from .whatsapp_service import send_registration_confirmation




import logging

logger = logging.getLogger(__name__)

class SubscribedUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscribedUsers
        fields = ['id', 'email', 'created_date']


class EventsSerializer(serializers.ModelSerializer):
    image_field = serializers.ImageField(write_only=True, required=False)  # To handle image upload
    image_url = serializers.SerializerMethodField() # To return the S3 URL

    class Meta:
        model = Events
        fields = ['id','name','category','description',
                  'image_url','image_field','date','location',
                  'organizer','contact_email','is_virtual']
        extra_kwargs = {
            'image_url': {'read_only': True}  # This field will store the S3 URL and is read-only
        }
    def get_image_url(self,obj):
        """Return the full s3 url for the image"""
        if obj.image_url:
            if obj.image_url.startswith('http'): # if it's already a full URL
                return obj.image_url
            # if it's just the path,Construct the full url
            return f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{obj.image_url}"
        return None
   

    def create(self, validated_data):
        # Extract `image_field` from the validated data
        image_file = validated_data.pop('image_field', None)
        print("Starting creating process....")
        print(f"Image file is in validated_data:{image_file}")
        # Create the event instance
        event_instance = Events.objects.create(**validated_data)
        print(f"Event instance created with ID: {event_instance.id}")


        # Handle S3 upload if an image is provided
        if image_file:
            try:
                print(f"Attempting S3 upload for file: {image_file.name}")
        
                s3_client = boto3.client(
                    's3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_S3_REGION_NAME
                )

                # Generate a unique file name
                filename = f"event_images/{uuid.uuid4()}_{image_file.name}"
                print(f"Generated filename: {filename}")

                # Reset file pointer
                image_file.seek(0)

                # Upload the file to S3
                print("Starting S3 upload...")
                s3_client.upload_fileobj(
                    image_file,
                    settings.AWS_STORAGE_BUCKET_NAME,
                    filename,
                    ExtraArgs={
                        'ContentType': image_file.content_type
                    }
                )
                print("S3 upload completed")

               
                # store just the path,the SerializerMethodField will construct the full url
                event_instance.image_url = filename
                event_instance.save()


                # Set the public S3 URL in the `image` field
                #event_instance.image = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{filename}"
                #event_instance.save()
            except Exception as e:
                    print(f"Error uploading to S3: {str(e)}")
                    import traceback
                    print(f"Traceback: {traceback.format_exc()}")
                    raise serializers.ValidationError(f"Failed to upload image to S3: {str(e)}")
        return event_instance
        
   

    def update(self, instance, validated_data):
        image_file = validated_data.pop('image_field', None)

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if image_file:
            try:
                s3_client = boto3.client(
                    's3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_S3_REGION_NAME
                )

                # Delete old image if it exists and isn't the default
                if instance.image_url and 'default.png' not in instance.image_url:
                    old_key = instance.image_url.split('.com/')[-1]
                    try:
                        s3_client.delete_object(
                            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                            Key=old_key
                        )
                    except Exception as e:
                        print(f"Warning: Failed to delete old image: {str(e)}")

                # Generate unique filename
                filename = f"event_images/{uuid.uuid4()}_{image_file.name}"
                image_file.seek(0)

                # Upload new image
                s3_client.upload_fileobj(
                    image_file,
                    settings.AWS_STORAGE_BUCKET_NAME,
                    filename,
                    ExtraArgs={'ContentType': image_file.content_type}
                )

                # Update the image URL
                s3_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{filename}"
                instance.image_url = s3_url

            except Exception as e:
                print(f"Error uploading to S3: {str(e)}")
                raise serializers.ValidationError(f"Failed to upload image to S3: {str(e)}")

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

            # send WhatsApp notification
            send_registration_confirmation.delay(str(registration.uid))

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