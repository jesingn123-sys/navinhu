import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

logger = logging.getLogger(__name__)

def send_email_notification(booking_details):
    """Send email notification to clinic owner about new booking"""
    try:
        sender = os.getenv('EMAIL_USER')
        password = os.getenv('EMAIL_PASSWORD')
        receiver = os.getenv('CLINIC_EMAIL')

        # If no email credentials, skip silently
        if not sender or not password or not receiver:
            return {'success': False, 'error': 'Email credentials not configured'}

        message = f"""
SMILE DENTAL & IMPLANT CLINIC
New Appointment Booked!

Patient Name : {booking_details.get('name')}
Phone Number : {booking_details.get('phone')}
Service      : {booking_details.get('service')}
Date         : {booking_details.get('date')}
Time         : {booking_details.get('time')}
Message      : {booking_details.get('message') or 'None'}

Please confirm the appointment by calling the patient.
        """

        msg = MIMEMultipart()
        msg['Subject'] = f"New Appointment - {booking_details.get('name')} - {booking_details.get('date')}"
        msg['From'] = sender
        msg['To'] = receiver
        msg.attach(MIMEText(message, 'plain'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender, password)
            smtp.sendmail(sender, receiver, msg.as_string())

        logger.info("Email notification sent successfully!")
        return {'success': True}

    except Exception as e:
        logger.error(f"Email error: {str(e)}")
        return {'success': False, 'error': str(e)}
