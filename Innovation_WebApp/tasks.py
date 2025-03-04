# events/tasks.py
from celery import shared_task

from Innovation_WebApp.models import EventRegistration
from .whatsapp_service import InfobipWhatsAppService
#from .models import EventRegistration
from datetime import datetime, timedelta
import logging
logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,  # 1 minute delay between retries
    autoretry_for=(Exception,),
    retry_backoff=True
)
def send_registration_confirmation(self, registration_id):
    """
    Send registration confirmation via WhatsApp
    Includes retry logic and better error handling
    """
    from .models import EventRegistration
    
    try:
        # Get registration with related event data
        registration = EventRegistration.objects.select_related('event').get(uid=registration_id)
        
        # Initialize WhatsApp service
        service = InfobipWhatsAppService()
        
        # Prepare message placeholders
        placeholders = [
            registration.full_name,
            registration.event.name,
            str(registration.ticket_number),
            registration.event.date.strftime("%Y-%m-%d %H:%M")
        ]
        
        # Format phone number (remove any spaces and ensure it starts with country code)
        phone_number = registration.phone_number.strip().replace(" ", "")
        if not phone_number.startswith('+'):
            phone_number = '+' + phone_number
        
        # Send the message
        result = service.send_template_message(
            to_number=phone_number,
            template_name="event_registration_confirmation",
            placeholders=placeholders
        )
        
        if not result.get('success', False):
            error_msg = result.get('error', 'Unknown error')
            logger.error(f"Failed to send WhatsApp message: {error_msg}")
            raise Exception(f"WhatsApp message sending failed: {error_msg}")
        
        return result
        
    except EventRegistration.DoesNotExist:
        logger.error(f"Registration {registration_id} not found")
        # Don't retry for non-existent registrations
        return {'success': False, 'error': f"Registration {registration_id} not found"}
        
    except Exception as e:
        logger.error(f"Error sending WhatsApp message: {str(e)}")
        # This will trigger a retry if we haven't exceeded max_retries
        raise self.retry(exc=e)

@shared_task
def send_event_reminder():
    """Send event reminders via WhatsApp"""
    tomorrow = datetime.now().date() + timedelta(days=1)
    
    try:
        registrations = EventRegistration.objects.select_related('event').filter(
            event__date__date=tomorrow
        )
        
        service = InfobipWhatsAppService()
        results = []
        
        for registration in registrations:
            placeholders = [
                registration.full_name,
                registration.event.name,
                registration.event.date.strftime("%H:%M"),
                #registration.event.venue,
                str(registration.ticket_number)
            ]
            
            result = service.send_template_message(
                to_number=registration.phone_number,
                template_name="event_reminder",
                placeholders=placeholders
            )
            
            results.append({
                'registration_id': str(registration.uid),
                'result': result
            })
            
        return results
        
    except Exception as e:
        return {'success': False, 'error': str(e)}