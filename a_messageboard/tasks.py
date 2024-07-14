from celery import shared_task
from django.core.mail import EmailMessage

@shared_task
def send_email_taks(subject, body, subscriber):
    email = EmailMessage(subject, body, to=[subscriber.email])
    email.send()
