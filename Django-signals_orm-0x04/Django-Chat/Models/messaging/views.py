# Django-Chat/Models/messaging/views.py

from django.shortcuts import render
from .models import Message
from django.contrib.auth.decorators import login_required

@login_required
def threaded_conversations(request):
    # Top-level messages only (not replies)
    messages = Message.objects.filter(
        parent_message__isnull=True
    ).select_related('sender', 'receiver').prefetch_related(
        'replies__sender', 'replies__receiver'
    )

    return render(request, 'messaging/threaded.html', {'messages': messages})

