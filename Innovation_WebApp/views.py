from rest_framework import viewsets, views, status,generics,serializers
from rest_framework.response import Response
from .serializers import SubscribedUsersSerializer, EventsSerializer,CommentSerializer,CommentUpdateSerializer
from account.models import NormalUser
from .models import SubscribedUsers, Events,Comment
from django.core.mail import send_mail, EmailMessage
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.files import File
import base64
from uuid import UUID

# class EventsViewSet(viewsets.ModelViewSet):
#     queryset = Events.objects.all()
#     serializer_class = EventsSerializer

#     def create(self, request, *args, **kwargs):
#         image_file = request.FILES.get('image')
#         if image_file:
#             # Convert the image to base64 string
#             image_data = image_file.read()
#             base64_image = base64.b64encode(image_data).decode("utf-8")
#             request.data['image'] = base64_image
#         return super().create(request, *args, **kwargs)


#this is the event with s3 functionality    
class EventViewSet(viewsets.ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer

# class NewsletterSendView(views.APIView):
#     #permission_classes = [IsAdminUser]
#
#     def post(self, request):
#         subject = request.data.get('subject')
#         receivers = request.data.get('receivers')
#         message = request.data.get('message')
#
#         receivers_list = [receiver.strip() for receiver in receivers.split(',')]
#
#         user_email = request.user.email if request.user.is_authenticated and request.user.email else 'default@example.com'
#         mail = EmailMessage(subject, message, f"Meru University Science Innovators Club <{user_email}>", bcc=receivers_list)
#         mail.content_subtype = 'html'
#
#         if mail.send():
#             return Response({'message': 'Email sent successfully'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'message': 'There was an error sending the email'}, status=status.HTTP_400_BAD_REQUEST)

class NewsletterSendView(views.APIView):
    def post(self, request):
        subject = request.data.get('subject')
        message = request.data.get('message')

        # Retrieve all subscribed email addresses
        subscribed_emails = list(SubscribedUsers.objects.values_list('email', flat=True))

        user_email = request.user.email if request.user.is_authenticated and request.user.email else 'default@example.com'
        mail = EmailMessage(subject, message, f"Meru University Science Innovators Club <{user_email}>", bcc=subscribed_emails)
        mail.content_subtype = 'html'

        if mail.send():
            return Response({'message': 'Email sent successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'There was an error sending the email'}, status=status.HTTP_400_BAD_REQUEST)

class SubscribeView(views.APIView):
    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({'message': 'Please enter a valid email address to subscribe to our Newsletters!'}, status=status.HTTP_400_BAD_REQUEST)

        if SubscribedUsers.objects.filter(email=email).exists():
            return Response({'message': f'{email} email address is already a subscriber'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_email(email)
        except ValidationError as e:
            return Response({'message': e.messages[0]}, status=status.HTTP_400_BAD_REQUEST)

        subscribe_model_instance = SubscribedUsers(email=email)
        subscribe_model_instance.save()

        return Response({'message': f'{email} email was successfully subscribed to our newsletter!'}, status=status.HTTP_201_CREATED)

class ContactView(views.APIView):
    def post(self, request):
        message_name = request.data.get('name')
        message_email = request.data.get('email')
        message = request.data.get('message')

        send_mail(
            message_name,
            message,
            message_email,
            ['ondeyostephen0@gmail.com']
        )

        return Response({'message_name': message_name}, status=status.HTTP_200_OK)
    

#COMMENTS APIS
class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


    def perform_create(self, serializer):
        post_id = serializer.validated_data.get('post')
        users_id = serializer.validated_data.get('user')

        if post_id is None:
            raise serializers.ValidationError("Post ID is required.")
        if users_id is None:
            raise serializers.ValidationError("User ID is required.")

        print(f"Received post_id: {post_id} of type {type(post_id)}, user_id: {users_id} of type {type(users_id)}")

        try:
            post = Events.objects.get(id=post_id)
        except Events.DoesNotExist:
            raise serializers.ValidationError({"error": f"Invalid post. No event with id {post_id} exists."})

        try:
            print(users_id)
            user = NormalUser.objects.get(user_id=users_id)
        except NormalUser.DoesNotExist:
            print(users_id)
            user = NormalUser.objects.get(user_id=users_id)
            raise serializers.ValidationError({"error": f"Invalid user. No user with id {users_id} exists."})

        serializer.save(post=post, user=user)


    # def perform_create(self, serializer):
    
    #     post_id = serializer.validated_data.get('post')
    #     user_id = serializer.validated_data.get('user')

    #     if post_id is None:
    #         raise serializers.ValidationError("post is required.")
    #     if user_id is None:
    #         raise serializers.ValidationError("user is required.")

    #     try:
    #         post = Events.objects.get(id=post_id)
    #     except Events.DoesNotExist as e:
    #         raise serializers.ValidationError(
    #             {
    #                 "error":f"Invalid post. {str(e)}"
    #             }
    #         )

    #     try:
    #         user = NormalUser.objects.get(user_id=user_id)
    #     except NormalUser.DoesNotExist as e:
    #         raise serializers.ValidationError(
    #             {
    #                 "error":f"Invalid post. {str(e)}"
    #             }
    #         )

    #     serializer.save(post=post, user=user)





# Update a Comment
class CommentUpdateView(generics.UpdateAPIView):
    serializer_class = CommentUpdateSerializer

    def get_object(self):
        comment_id = self.request.data.get('id')
        user_id = self.request.data.get('user')
        
        if not comment_id:
            raise serializers.ValidationError({"id": "This field is required."})
        if not user_id:
            raise serializers.ValidationError({"user": "This field is required."})

        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            raise serializers.ValidationError({"error": "Comment not found."})

        try:
            user_uuid = UUID(user_id) if isinstance(user_id, str) else user_id
            user = NormalUser.objects.get(user_id=user_uuid)
            
            if comment.user.user_id != user.user_id:
                raise serializers.ValidationError({"authorization": "You are not authorized to edit this comment."})
            return comment
        except (NormalUser.DoesNotExist, ValueError):
            raise serializers.ValidationError({"user": "User not found."})
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})

    def perform_update(self, serializer):
        # The user field will now be a NormalUser instance thanks to validate_user
        serializer.save()
        

# Delete a Comment
class CommentDeleteView(generics.DestroyAPIView):
    serializer_class = CommentSerializer
    

    def get_object(self):
        comment_id = self.request.data.get('id')
        if not comment_id:
            raise serializers.ValidationError({"id": "This field is required."})

        try:
            comment = Comment.objects.get(id=comment_id, user=self.request.user)
        except Comment.DoesNotExist:
            raise serializers.ValidationError({"id": "Comment not found or you do not have permission to delete it."})

        return comment
    # Get all Comments
class CommentListView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        for comment in response.data['results']:
            comment_instance = Comment.objects.get(text=comment['text'])
            comment['id'] = comment_instance.id
            comment['user'] = comment_instance.user.user_id
            comment['post'] = comment_instance.post.id
        return response

