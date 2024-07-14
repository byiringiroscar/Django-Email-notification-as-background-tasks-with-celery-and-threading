from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

# Create your views here.

@login_required
def messageboard_view(request):
    messageboard = get_object_or_404(MessageBoard, id=1)
    form = MessageCreateForm()

    if request.method == 'POST':
        form = MessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.messageboard = messageboard
            message.author = request.user
            message.save()
            return redirect('messageboard')


    context = {
        'messageboard': messageboard,
        'form': form,
    }
    return render(request, 'a_messageboard/index.html', context)