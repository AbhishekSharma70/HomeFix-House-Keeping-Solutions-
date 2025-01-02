import os

class Config:
    # Twilio configuration
    SECRET_KEY=''
    CELERY_BROKER_URL='redis://localhost:6379/0'
    CELERY_RESULT_BACKEND='redis://localhost:6379/0'
    TWILIO_ACCOUNT_SID = ''
    TWILIO_AUTH_TOKEN = ''
    TWILIO_PHONE_NUMBER = ''

    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USE_SSL=False
    MAIL_USERNAME=''
    MAIL_PASSWORD=''
    MAIL_DEFAULT_SENDER=''


