from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
import qrcode
from io import BytesIO
import os
from datetime import datetime
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A6  # Using A6 for a smaller ticket size
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch

def generate_ticket_pdf(rsvp, event):
    """
    Generate a compact ticket as a PDF file using the RSVP and event information
    """
    # Generate smaller QR code
    qr = qrcode.QRCode(
        version=1,
        box_size=5,  # Reduced box size
        border=2      # Reduced border
    )
    qr_data = f"Name: {rsvp.full_name}\nEvent: {event.title}\nID: {rsvp.id}"
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    # Save QR code to temporary buffer
    temp_qr = BytesIO()
    qr_image.save(temp_qr, format='PNG')
    temp_qr.seek(0)
    
    # Create PDF with A6 size (105mm × 148mm)
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=A6)
    width, height = A6  # A6 dimensions
    
    # Add a border
    c.rect(10, 10, width-20, height-20)
    
    # Add event title
    c.setFont("Helvetica-Bold", 14)
    c.drawString(20, height-30, event.title[:35])  # Limit title length
    
    # Add event details with smaller font
    c.setFont("Helvetica", 10)
    date_str = event.date.strftime('%B %d, %Y')
    c.drawString(20, height-50, f"Date: {date_str}")
    c.drawString(20, height-65, f"Attendee: {rsvp.full_name[:30]}")  # Limit name length
    c.drawString(20, height-80, f"Ticket ID: #{rsvp.id}")
    
    # Add QR code - smaller and positioned to the right
    img = ImageReader(temp_qr)
    qr_size = 1 * inch  # 1 inch QR code
    c.drawImage(img, width-qr_size-20, height-100, width=qr_size, height=qr_size)
    
    # Add footer text
    c.setFont("Helvetica-Bold", 8)
    c.drawString(20, 25, "Please present this ticket at the event entrance")
    
    c.showPage()
    c.save()
    
    pdf_buffer.seek(0)
    return pdf_buffer

def send_rsvp_confirmation_email(rsvp, event):
    """
    Send confirmation email with ticket attachment to the RSVP email address
    """
    subject = f"Your Ticket for {event.title}"
    
    context = {
        'name': rsvp.full_name,
        'event_title': event.title,
        'event_date': event.date.strftime('%B %d, %Y at %I:%M %p'),
        'event_location': getattr(event, 'location', 'TBD'),
    }
    
    email_body = render_to_string('emails/rsvp_confirmation.html', context)
    
    email = EmailMessage(
        subject=subject,
        body=email_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[rsvp.email],
    )
    email.content_subtype = "html"
    
    # Generate and attach the ticket
    ticket_pdf = generate_ticket_pdf(rsvp, event)
    email.attach(
        f'ticket_{event.title}_{rsvp.id}.pdf',
        ticket_pdf.getvalue(),
        'application/pdf'
    )
    
    email.send()