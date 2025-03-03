from django.core.mail import send_mail

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
    message = f"""
    Event Ticket Details:
    Ticket Number: {ticket_details['ticket_number']}
    Event: {ticket_details['event_name']}
    Date: {ticket_details['event_date']}
    Location: {ticket_details['event_location']}
    Registered By: {ticket_details['participant_name']}
    """
    
    send_mail(
        subject,
        message,
        'ondeyostephen0@gmail.com',  # From email
        [registration.email],    # To email
        fail_silently=False,
    )

    