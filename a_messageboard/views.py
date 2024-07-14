from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *

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
    

