from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .models import *
from datetime import datetime

@shared_task(name='email_notification')
def send_email_taks(subject, body, email_address):
    email = EmailMessage(subject, body, to=[email_address])
    email.send()
    return email_address

@shared_task(name='monthly_newsletter')
def send_newsletter():
    subject = 'Monthly Newsletter'
    subscribers = MessageBoard.objects.get(id=1).subscribers.all()
    for subscriber in subscribers:
        body = render_to_string('a_messageboard/newsletter.html', {'name': subscriber.profile.name})
        email = EmailMessage(subject, body, to=[subscriber.email])
        email.content_subtype = "html"
        email.send()
    current_month = datetime.now().strftime('%B')
    subscriber_count = subscribers.count()
    return f'{current_month} Newsletter sent to {subscriber_count} subs'
