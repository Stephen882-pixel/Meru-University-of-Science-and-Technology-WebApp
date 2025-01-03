from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Innovation_WebApp.models import Events
from .serializers import RSVPSerializer,EventRSVPSerializer
from .utils import send_rsvp_confirmation_email

# class RSVPCreateView(APIView):
#     def post(self, request):
#         event_id = request.data.get('eventId')
#         try:
#             event = Events.objects.get(id=event_id)
#         except Events.DoesNotExist:
#             return Response({'error': 'Event not found'}, status=404)

#         rsvp_data = {
#             'full_name': request.data.get('fullName'),
#             'email': request.data.get('email'),
#             'phone_number': request.data.get('phoneNumber'),
#             'attending': request.data.get('attending', True)
#         }
        
#         serializer = RSVPSerializer(data=rsvp_data)
#         if serializer.is_valid():
#             serializer.save(event=event)
#             return Response(EventRSVPSerializer(event).data)
#         return Response(serializer.errors, status=400)
    

class RSVPCreateView(APIView):
    def post(self, request):
        event_id = request.data.get('eventId')
        try:
            event = Events.objects.get(id=event_id)
        except Events.DoesNotExist:
            return Response({'error': 'Event not found'}, status=404)
            
        rsvp_data = {
            'full_name': request.data.get('fullName'),
            'email': request.data.get('email'),
            'phone_number': request.data.get('phoneNumber'),
            'attending': request.data.get('attending', True)
        }
        
        serializer = RSVPSerializer(data=rsvp_data)
        if serializer.is_valid():
            rsvp = serializer.save(event=event)
            # Send confirmation email with ticket
            send_rsvp_confirmation_email(rsvp, event)
            return Response(EventRSVPSerializer(event).data)
        return Response(serializer.errors, status=400)