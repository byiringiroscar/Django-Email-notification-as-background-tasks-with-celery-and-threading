from celery import shared_task
from django.core.mail import EmailMessage

@shared_task(name='email_notification')
def send_email_taks(subject, body, email_address):
    email = EmailMessage(subject, body, to=[email_address])
    email.send()
    return email_address
