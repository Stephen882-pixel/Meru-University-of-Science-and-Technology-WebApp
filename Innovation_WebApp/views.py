from rest_framework import viewsets, views, status
from rest_framework.response import Response
from .serializers import SubscribedUsersSerializer, EventsSerializer
from .models import SubscribedUsers, Events
from django.core.mail import send_mail, EmailMessage
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.files import File
import base64

class EventsViewSet(viewsets.ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer

    def create(self, request, *args, **kwargs):
        image_file = request.FILES.get('image')
        if image_file:
            # Convert the image to base64 string
            image_data = image_file.read()
            base64_image = base64.b64encode(image_data).decode("utf-8")
            request.data['image'] = base64_image
        return super().create(request, *args, **kwargs)

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