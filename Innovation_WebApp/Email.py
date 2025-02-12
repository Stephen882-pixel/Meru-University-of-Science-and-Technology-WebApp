from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string

def send_ticket_email(registration):
    ticket_details = {
        'ticket_number': str(registration.ticket_number),
        'event_name': registration.event.name,
        'event_date': registration.event.date,
        'participant_name': registration.full_name,
        'event_location': registration.event.location,
        'registration_timestamp': registration.registration_timestamp
    }

    subject = f'Event Ticket: {registration.event.name}'
    message = render_to_string('emails/ticket_email.hml',ticket_details) 

    email = EmailMessage(
        subject=subject,
        body=message,
        from_email='ondeyostephen0@gmail.com',
        to=[registration.email]
    )
    email.content_subtype = "html"
    
    
    email.send()
    