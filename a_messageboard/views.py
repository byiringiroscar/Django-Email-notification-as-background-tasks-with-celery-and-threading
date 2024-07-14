from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def messageboard_view(request):
    return render(request, 'a_messageboard/index.html')
