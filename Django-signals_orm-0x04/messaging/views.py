from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import messages

@login_required
def delete_user(request):
    user = request.user
    user.delete()
    messages.success(request, "Your account and related data have been deleted.")
    return redirect('home')  # Redirect to a suitable view after deletion

@login_required
def threaded_conversations(request):
    # Top-level messages only (not replies)
    messages = Message.objects.filter(
        parent_message__isnull=True
    ).select_related('sender', 'receiver').prefetch_related(
        'replies__sender', 'replies__receiver'
    )

    return render(request, 'messaging/threaded.html', {'messages': messages})

@login_required
def unread_inbox(request):
    unread_messages = Message.unread.for_user(request.user)
    return render(request, 'messaging/unread_inbox.html', {'unread_messages': unread_messages})
