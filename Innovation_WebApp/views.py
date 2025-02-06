import csv
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

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.pagination import PageNumberPagination
import logging


class EventPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'message':'Events retrieved successfuly',
            'status':'success',
            'data':{
                'count':self.page.paginator.count,
                'next':self.get_next_link(),
                'previous':self.get_previous_link(),
                'results':data
            }
        })

#this is the event with s3 functionality   
@method_decorator(csrf_exempt, name='dispatch') 
class EventViewSet(viewsets.ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer
    pagination_class = EventPagination

   
    def create(self,request,*args,**kwargs):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            event_instance = serializer.create(serializer.validated_data)
            return Response({
                'message':'Event Created successfully',
                'status':'success',
                'data':EventsSerializer(event_instance).data
            },status=status.HTTP_201_CREATED)
        return Response({
            'message':'Event Creation Failed',
            'status':serializer.errors,
            'data':None
        },status=status.HTTP_400_BAD_REQUEST)
    
    def update(self,request,*args,**kwargs):
        partial = kwargs.pop('partial',False)
        instance = self.get_object()
        serializer = self.get_serializer(instance,data=request.data,partial=partial)

        if serializer.is_valid():
            event_instance = serializer.save()
            return Response({
                'message':'Event Updated Successfully',
                'status':'success',
                'data':EventsSerializer(event_instance).data
            },status=status.HTTP_200_OK)
        
        return Response({
            'message':'Event update failed',
            'status':'error',
            'errors':serializer.errors,
            'data':None
        },status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request, *args,**kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page,many=True)
            return self.get_paginated_response(serializer.data)
        # Fallback incase pagination fails or is disabled
        serializer=self.get_serializer(queryset,many=True)

        return Response({
            'message':'Events retrieved successfully',
            'status':'success',
            'data':{
                'count':queryset.count(),
                'next':None,
                'previous':None,
                'results':serializer.data
            }
        },status=status.HTTP_200_OK)
    

    def retrieve(self, request, *args, **kwargs):
        try:
            
            # Get the even ID from url kwargs
            event_id = kwargs.get('pk')
            if not event_id:
                return Response({
                    'message':'Event ID not provided',
                    'status':'failed',
                    'data':None
                },status=status.HTTP_400_BAD_REQUEST)
            
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({
                'message':'Event details fetched successfully',
                'status':'success',
                'data':serializer.data
            },status=status.HTTP_200_OK)
        except Exception as e:
            
            return Response({
                'message':'Error fetching the event',
                'status':'failed',
                'data':None
            },status=status.HTTP_400_BAD_REQUEST)
    



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

    def get_queryset(self):
        event_pk = self.kwargs.get('event_pk')
        if event_pk:
            return EventRegistration.objects.filter(event_id=event_pk)
        return super().get_queryset()
    
    @action(detail=False, methods=['get'], url_path='user_id')
    def get_user_registration(self,request,event_pk=None):
        try:
            if not event_pk:
                return Response({
                    'message':'Event ID missing',
                    'status':'failed',
                    'data':None
                },status=status.HTTP_400_BAD_REQUEST)
            registration = EventRegistration.objects.filter(
                event_id=event_pk,
                email=request.user.email
            ).first()

            if not registration:
                return Response({
                    'message':'No registration found for this user in this event',
                    'status':'failed',
                    'data':None
                },status=status.HTTP_400_BAD_REQUEST)
            serializer = self.get_serializer(registration)
            return Response({
                'message':'User registration details retrieved successfully',
                'status':'success',
                'data':serializer.data
            },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'message':f'Error retrieving registration: {str(e)}',
                'status':'failed',
                'data':None
            })
    
    def list(self,request,*args,**kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page,many=True)
                paginated_data = self.paginator.get_paginated_response(serializer.data)

                return Response({
                    'message':'Event registrations retrieved successfully',
                    'status':'success',
                    'data':{
                        'count':paginated_data.data['count'],
                        'next':paginated_data.data['next'],
                        'previous':paginated_data.data['previous'],
                        'results':paginated_data.data['results']
                    }
                },status=status.HTTP_200_OK)
            serializer = self.get_serializer(queryset,many=True)
            return Response({
                'message':'Event registrations retrieved successfully',
                'status':'success',
                'data':{
                    'count':len(serializer.data),
                    'next':None,
                    'previous':None,
                    'data':serializer.data
                }
            },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'message':f'Error retreiving registrations:{str(e)}',
                'status':'failed',
                'data':None
            },status=status.HTTP_400_BAD_REQUEST)
        

    def create(self, request, *args, **kwargs):
        event_pk = self.kwargs.get('event_pk')
        if not event_pk:
            return Response({
                'message': 'Event ID is missing in the request URL',
                'status': 'failed',
                'data': None
            }, status=status.HTTP_401_UNAUTHORIZED)

        mutable_data = request.data.copy()
        mutable_data['event'] = event_pk
        serializer = self.get_serializer(data=mutable_data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Successfully registered for the event',
                'status': 'Success',
                'data': None
            }, status=status.HTTP_200_OK)
        
        error_messages = "\n".join(
            f"{field}: {', '.join(errors)}" for field, errors in serializer.errors.items()
        )
        return Response({
            'message': f"Event Registration failed: {error_messages}",
            'status': 'failed',
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)
    

    
    @action(detail=False, methods=['get'], url_path='export')
    def export_registrations(self, request, event_pk=None):
        if not event_pk:
            return Response({"error": "Event ID is required"}, status=400)
        
        registrations = EventRegistration.objects.filter(event_id=event_pk)
    
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="event_{event_pk}_registrations.csv"'
    
        writer = csv.writer(response)
        writer.writerow((
            'UID', 
            'Full Name', 
            'Email', 
            'Course',
            'Educational Level',
            'Phone Number',
            'Expectations',
            'Registration Date',
            'Ticket Number'
        ))
    
        for registration in registrations:
            writer.writerow((
                registration.uid, 
                registration.full_name, 
                registration.email, 
                registration.course,
                registration.educational_level,
                registration.phone_number,
                registration.expectations,
                registration.registration_timestamp,
                registration.ticket_number
            ))
    
        return response

def send_registration_confirmation(registration):
    # Ticket email template
    subject = f'Event Ticket - {registration.event.title}'
    'Meru University Science Innovators Club <your_event_email@example.com>',
    message = render_to_string('ticket_email.html', {
        'registration': registration,
        'ticket_number': registration.ticket_number,
        'event': registration.event
    })
    
    # Use the recipient's email address
    recipient_email = registration.attendee.email  # Assuming you have the attendee's email
    
    send_mail(
        subject,
        message,
        'Meru University Science Innovators Club <your_event_email@example.com>',  # Sender name and email
        #[recipient_email],  # List of recipient emails
        html_message=message
    )



def create(self, validated_data):
    registration = super().create(validated_data)
    send_registration_confirmation(registration)
    return registration


class CommunityProfileViewSet(viewsets.ModelViewSet):
    queryset = CommunityProfile.objects.all().order_by('id')
    serializer_class = CommunityProfileSerializer

    def create(self,request,*args,**kwags):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
                return Response({
                    'message':'Community Created successfully',
                    'status':'success',
                    'data':serializer.data
                },status=status.HTTP_201_CREATED)

            error_messages = "\n".join(
                f"{field}:{', '.join(errors)}" for field, errors in serializer.errors.items()
            )
            return Response({
                'message':f'Community Creation failed: {error_messages}',
                'status':'failed',
                'data':None
            },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'message': f'Error creating community: {str(e)}',
                'status': 'failed',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)

    def list(self,request,*args,**kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page,many=True)
                paginated_data = self.paginator.get_paginated_response(serializer.data)

                return Response({
                    'message':'Communities retrieved successfully',
                    'status':'success',
                    'data':{
                        'count':paginated_data.data['count'],
                        'next':paginated_data.data['next'],
                        'previous':paginated_data.data['previous'],
                        'results':paginated_data.data['results']
                    }
                },status=status.HTTP_200_OK)
            serializer = self.get_serializer(queryset,many=True)
            return Response({
                'message':'Communities retrieved successfully',
                'status':'success',
                'data':serializer.data
            },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'message':f'Error retrieving communities',
                'status':'failed',
                'data':None
            },status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)

            return Response({
                'message':'Community retrieved successfully',
                'status':'success',
                'data':serializer.data
            },status=status.HTTP_200_OK)
        except CommunityProfile.DoesNotExist:
            return Response({
                'message':'Community not found',
                'status':'failed',
                'data':None
            },status=status.HTTP_400_BAD_REQUEST)



class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.filter(is_approved=True)
    serializer_class = TestimonialSerializer
    #permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)





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
                #return Response(session_serializer.data, status=status.HTTP_201_CREATED)
                return Response({
                    'message':'Session Updated Successfully',
                    'status':'success',
                    'data':session_serializer.data
                },status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'message':session_serializer.errors,
                    'status':'failed',
                    'data':None
                })
            

        except CommunityProfile.DoesNotExist:
            return Response({
                'message':'Commmunity not found',
                'status':'failed',
                'data':None
            },status=status.HTTP_400_BAD_REQUEST)
            #return Response({"detail": "Community not found."}, status=status.HTTP_404_NOT_FOUND)
        

    

class CommunityMembersView(APIView):
    def get(self, request, pk):
        try:
            community = CommunityProfile.objects.get(pk=pk)
        except CommunityProfile.DoesNotExist:
            return Response({"error": "Community not found"}, status=status.HTTP_404_NOT_FOUND)

        members = community.members.all()  # Fetch related members
        serializer = CommunityMemberSerializer(members, many=True)
        return Response({
            'message':'Members retrieved successfully',
            'status':'success',
            'data':serializer.data
        })
        #return Response(serializer.data, status=status.HTTP_200_OK)
    

class JoinCommunityView(APIView):
    def post(self, request, *args, **kwargs):
        community_id = kwargs.get('pk')  # Assuming URL pattern passes community ID
        
        try:
            community = CommunityProfile.objects.get(id=community_id)
        except CommunityProfile.DoesNotExist:
            return Response(
                {"error": "Community not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = CommunityJoinSerializer(data={
            'community': community.id,
            'name': request.data.get('name'),
            'email': request.data.get('email')
        })
        
        if serializer.is_valid():
            member = serializer.save(community=community)
            community.update_total_members()
            
            return Response({
                "message": "Successfully joined the community!",
                'status':'success',
                'data':None
                },status=status.HTTP_201_CREATED)
        return Response({
            'message':f'There was an error please try again: {serializer.errors}',
            'status':'failed',
            'data':None
        },status=status.HTTP_400_BAD_REQUEST)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)