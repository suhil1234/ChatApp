from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from chat.models import Thread


@login_required
def index(request):
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    context = {
        'Threads': threads
    }
    return render(request, 'chat/index.html', context)