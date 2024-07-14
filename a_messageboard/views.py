from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from .models import *
from .forms import *
import threading
from .tasks import *

# Create your views here.

@login_required
def messageboard_view(request):
    messageboard = get_object_or_404(MessageBoard, id=1)
    form = MessageCreateForm()

    if request.method == 'POST':
        if request.user in messageboard.subscribers.all():
            form = MessageCreateForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.messageboard = messageboard
                message.author = request.user
                message.save()

                send_email(message)
        else:
            messages.warning(request, 'You need to be Subscribed! ')
        return redirect('messageboard')




    context = {
        'messageboard': messageboard,
        'form': form,
    }
    return render(request, 'a_messageboard/index.html', context)


@login_required
def subscribe(request):
    messageboard = get_object_or_404(MessageBoard, id=1)
    if request.user not in messageboard.subscribers.all():
        messageboard.subscribers.add(request.user)
        messages.success(request, 'You are now Subscribed! ')
    else:
        messageboard.subscribers.remove(request.user)
        messages.success(request, 'You are now Unsubscribed! ')
    
    return redirect('messageboard')


# make sure to run celery worker when you are using celery

'''
celery -A a_core worker -P info  # this for single worker for lower workloads
celery -A a_core worker -P gevent  # this for multiple worker for higher workloads
celery -A a_core worker -P threads  # 

'''
def send_email(message):
    messageboard = message.messageboard
    subscribers = messageboard.subscribers.all()

    for subscriber in subscribers:
        subject = f'New Message from {message.author.profile.name}'
        body = f'Hello {message.author.profile.name}: {message.body} \n\nRegards from\nMy Message Board'
        send_email_taks.delay(subject, body, subscriber.email)



    

