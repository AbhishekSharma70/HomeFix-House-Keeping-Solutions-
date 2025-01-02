from twilio.rest import Client
from celery import Celery
from flask import current_app
from celery.schedules import crontab
import time




celery_app = Celery('tasks', broker='redis://127.0.0.1:6379/0')

account_sid = ''
auth_token = ''
twilio_client = Client(account_sid, auth_token)

TWILIO_WHATSAPP_NUMBER = 'whatsapp:+14155238886'  # This is the official Twilio sandbox WhatsApp number

celery_app.conf.beat_schedule = {
    'send_whatsapp_notifications_every_morning': {
        'task': 'tasks.send_whatsapp_notifications_task',  # The task to run
        'schedule': crontab(hour=18, minute=54),
    },
}

celery_app.conf.timezone = 'Asia/Kolkata'


@celery_app.task
def send_whatsapp_notifications_task():
    """
    A Celery task that triggers send_whatsapp_notifications from the Flask app.
    """
    try:
        # Access the Flask app context using current_app
        with app.app_context():  # Ensure the app context is available
            # Get the send_whatsapp_notifications function from the Flask app
            send_whatsapp_notifications = current_app.send_whatsapp_notifications
            send_whatsapp_notifications()  # Call the function
    except Exception as e:
        print(f"Error occurred while sending WhatsApp notifications: {str(e)}")


@celery_app.task
def send_whatsapp_message_to_professional(professional_phone_number, service_description, customer_name, customer_address, customer_pincode):
    try:
        
        message_body = (
            f"New Service Request from {customer_name}:\n\n"
            f"Description: {service_description}\n"
            f"Address: {customer_address}\n"
            f"Pincode: {customer_pincode}"
        )

        message = twilio_client.messages.create(
            body=message_body,
            from_=TWILIO_WHATSAPP_NUMBER,  # Twilio sandbox WhatsApp number
            to=f'whatsapp:+91{professional_phone_number}'  # Professional's phone number with country code
        )
        print(f'WhatsApp message sent: {message.sid}')
    except Exception as e:
        print(f'Failed to send WhatsApp message: {str(e)}')


@celery_app.task
def send_whatsapp_message(professional, request_type, service_details):
    
    try:
        message_body = (
            f"New {request_type} for you:\n\n"
            f"Description: {service_details.get('description', 'N/A')}\n"
            f"Customer Name: {service_details.get('customer_name', 'N/A')}\n"
            f"Address: {service_details.get('customer_address', 'N/A')}\n"
            f"Pincode: {service_details.get('customer_pincode', 'N/A')}\n\n"
            f"Please accept or reject the request as soon as possible."
        )

        message = twilio_client.messages.create(
            body=message_body,
            from_=TWILIO_WHATSAPP_NUMBER,
            to=f'whatsapp:+91{professional.phone_number}'  # Assuming 'phone_number' is a field in the Professional model
        )
        print(f'WhatsApp message sent to {professional.name}: {message.sid}')
    except Exception as e:
        print(f'Failed to send WhatsApp message to {professional.name}: {str(e)}')