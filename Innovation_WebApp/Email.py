from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

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
    html_message = render_to_string('email/send_email.html', {'ticket_details': ticket_details})
    plain_message = strip_tags(html_message)
    

    email = EmailMultiAlternatives(
        subject,
        plain_message,
        'ondeyostephen0@gmail.com',  # From email

        [registration.email]  # To email
    )
    email.attach_alternative(html_message, "text/html")
    email.send(fail_silently=False)

