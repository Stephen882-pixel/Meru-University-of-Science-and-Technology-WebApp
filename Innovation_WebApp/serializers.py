from rest_framework import serializers
from .models import SubscribedUsers, Events
import boto3
from django.conf import settings
import uuid


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