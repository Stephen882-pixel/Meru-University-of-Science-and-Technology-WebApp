# whatsapp_service.py
import http.client
import json
import uuid
from django.conf import settings
from celery import shared_task

class InfobipWhatsAppService:
    def __init__(self):
        self.host = settings.INFOBIP_HOST
        self.api_key = settings.INFOBIP_API_KEY
        self.sender = settings.INFOBIP_SENDER_NUMBER

    def send_template_message(self,to_number,template_name,placeholders=None):

        """
        send a whatsApp template message using Infobip API

        Args:
            to_number (str):Recipient's phone number
            template_name (str): Name of the approved template
            placeholders (list): List of placeholder values for the template
        """
        conn = http.client.HTTPSConnection(self.host)

        message_data = {
            "messages": [
                {
                    "from": self.sender,
                    "to": to_number,
                    "messageId": str(uuid.uuid4()),
                    "content": {
                        "templateName": template_name,
                        "templateData": {
                            "body": {
                                "placeholders": placeholders or []
                            }
                        },
                        "language": "en"
                    }
                }
            ]
        }

        headers = {
            'Authorization':f'App {self.api_key}',
            'Content-Type':'application/json',
            'Accept':'application/json'
        }

        try:
            conn.request(
                "POST",
                "/whatsapp/1/message/template",
                json.dumps(message_data),
                headers
            )
            response = conn.getresponse()
            response_data = json.loads(response.read().decode("utf-8"))

            return {
                "success":response.status==200,
                "response":response_data
            }
        except Exception as e:
            print(f"Error sending whatsApp message: {str(e)}")
            return {'success':False,'Error':str(e)}
        finally:
            conn.close

@shared_task
def send_registration_confirmation(registration_id):
    """Send registration confirmation via WhatsApp"""
    from .models import EventRegistration
    

    try:
        registration = EventRegistration.objects.select_related('event').get(uid=registration_id)
        service = InfobipWhatsAppService()

        # Format event details to include ticket number and date
        event_details = f"{registration.event.name} (Ticket #{registration.ticket_number}) on {registration.event.date.strftime('%Y-%m-%d %H:%M')}"

        placeholders = [
            registration.full_name,
            event_details
        ]


        result = service.send_template_message(
            to_number=registration.phone_number,
            template_name="confirmation_reservation",  # Update this to match your template name in Infobip
            placeholders=placeholders
        )
        print("Infobip Response:", result)
        

        if not result['success']:
            print(f"failef to send a whatsapp message: {result.get('error')}")

    except EventRegistration.DoesNotExist:
        print(f"Registration {registration_id} not found")

@shared_task
def send_event_reminder():
    """Send event reminders via WhatsApp"""
    from .models import EventRegistration
    from datetime import datetime,timedelta

    # Get regisrations for events happening tommorow
    tomorrow = datetime.now().date() + timedelta(days=1)
    registrations = EventRegistration.objects.select_related('event').filter(
        event__date__date=tomorrow
    )

    service = InfobipWhatsAppService()

    for registration in registrations:
         # Format event details to include time and ticket number
        event_details = f"{registration.event.name} tomorrow at {registration.event.date.strftime('%H:%M')} (Ticket #{registration.ticket_number})"

        placeholders = [
            registration.full_name,
            event_details
        ]


        result = service.send_template_message(
            to_number=registration.phone_number,
            template_name="confirmation_reservation",  # Use the same template for consistency
            placeholders=placeholders
        )
        
        if not result['success']:
            print(f"Failed to send reminder to {registration.full_name}: {result.get('error')}")