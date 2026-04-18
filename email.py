

import smtplib
import os
from email.mime.text import MIMEText
import logging

logger = logging.getLogger(__name__)

def send_email_notification(booking_details):
    try:
        sender = os.getenv('EMAIL_USER')
        password = os.getenv('EMAIL_PASSWORD')
        receiver = os.getenv('CLINIC_EMAIL')

        message = f"""
New Appointment Booked!

Patient: {booking_details.get('name')}
Phone: {booking_details.get('phone')}
Service: {booking_details.get('service')}
Date: {booking_details.get('date')}
Time: {booking_details.get('time')}
Message: {booking_details.get('message')}
        """

        msg = MIMEText(message)
        msg['Subject'] = 'New Dental Appointment - Smile Dental!'
        msg['From'] = sender
        msg['To'] = receiver

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender, password)
            smtp.sendmail(sender, receiver, msg.as_string())

        logger.info("Email notification sent successfully!")
        return {'success': True}

    except Exception as e:
        logger.error(f"Email error: {str(e)}")
        return {'success': False, 'error': str(e)}