from django.http import HttpResponse
from rest_framework import viewsets, views, status,permissions
from rest_framework.response import Response
from .serializers import CommunityJoinSerializer, CommunityMemberSerializer, CommunitySessionSerializer, SubscribedUsersSerializer, EventsSerializer,EventRegistrationSerializer,CommunityProfileSerializer,TestimonialSerializer
from .models import SubscribedUsers, Events,EventRegistration,CommunityProfile,Testimonial
from django.core.mail import send_mail, EmailMessage
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.files import File
import base64
from rest_framework.decorators import action
import pandas as pd
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework.views import APIView



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
    


from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
import pandas as pd

class EventRegistrationViewSet(viewsets.ModelViewSet):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer

    @action(detail=False, methods=['GET'])
    def export_registrations(self, request):
        event_id = request.query_params.get('event_id')
    
        if not event_id:
            return Response({'error': 'Event ID is required'}, status=400)

    # Filter registrations for the specific event
        registrations = EventRegistration.objects.filter(event_id=event_id)
    
    
        registration_data = []
        for reg in registrations:
            reg_dict = {
                'full_name': reg.full_name,
                'email': reg.email,
                'age_bracket': reg.age_bracket,
                'course': reg.course,
                'educational_level': reg.educational_level,
                'phone_number': reg.phone_number,
                'ticket_number': str(reg.ticket_number),
                'registration_timestamp': reg.registration_timestamp.replace(tzinfo=None) if reg.registration_timestamp else None
            }
            registration_data.append(reg_dict)
    
  
        df = pd.DataFrame(registration_data)
    
  
        response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
         )
        response['Content-Disposition'] = f'attachment; filename=event_registrations_{event_id}.xlsx'
    
  
        df.to_excel(response, index=False)
    
        return response
    

def send_registration_confirmation(registration):
    # Ticket email template
    subject = f'Event Ticket - {registration.event.title}'
    message = render_to_string('ticket_email.html', {
        'registration': registration,
        'ticket_number': registration.ticket_number,
        'event': registration.event
    })
    
    send_mail(
        subject,
        message,
        'your_event_email@example.com',
        [registration.email],
        html_message=message
    )


def create(self, validated_data):
    registration = super().create(validated_data)
    send_registration_confirmation(registration)
    return registration


class CommunityProfileViewSet(viewsets.ModelViewSet):
    queryset = CommunityProfile.objects.all().order_by('id')
    serializer_class = CommunityProfileSerializer

    # def get_permissions(self):
    #     if self.action in ['create', 'update', 'partial_update', 'destroy']:
    #         permission_classes = [IsAdminUser]
    #     else:
    #         permission_classes = [AllowAny]
    #     return [permission() for permission in permission_classes]

class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.filter(is_approved=True)
    serializer_class = TestimonialSerializer
    #permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



# class CommunityCategoryViewSet(viewsets.ModelViewSet):
#     queryset = CommunityCategory.objects.all()
#     serializer_class = CommunityCategorySerializer
    
    # def get_permissions(self):
    #     if self.action in ['create', 'update', 'partial_update', 'destroy']:
    #         permission_classes = [IsAdminUser]
    #     else:
    #         permission_classes = [permissions.AllowAny]
    #     return [permission() for permission in permission_classes]


class SessionCreateView(APIView):
    def post(self, request, community_id):
        try:
            # Retrieve the community by its ID
            community = CommunityProfile.objects.get(id=community_id)
            
            # Serialize the session data
            session_serializer = CommunitySessionSerializer(data=request.data)
            
            if session_serializer.is_valid():
                # Save the session and associate it with the community
                session_serializer.save(community=community)
                return Response(session_serializer.data, status=status.HTTP_201_CREATED)
            return Response(session_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except CommunityProfile.DoesNotExist:
            return Response({"detail": "Community not found."}, status=status.HTTP_404_NOT_FOUND)
        

    

class CommunityMembersView(APIView):
    def get(self, request, pk):
        try:
            community = CommunityProfile.objects.get(pk=pk)
        except CommunityProfile.DoesNotExist:
            return Response({"error": "Community not found"}, status=status.HTTP_404_NOT_FOUND)

        members = community.members.all()  # Fetch related members
        serializer = CommunityMemberSerializer(members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class JoinCommunityView(APIView):
    def post(self, request, *args, **kwargs):
        print("POST request received")
        serializer = CommunityJoinSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Successfully joined the community!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)