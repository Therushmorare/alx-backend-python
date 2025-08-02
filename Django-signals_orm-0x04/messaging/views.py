from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.cache import cache_page
from django.shortcuts import render

@cache_page(60)
@login_required
def delete_user(request):
    user = request.user
    user.delete()
    messages.success(request, "Your account and related data have been deleted.")
    return redirect('home')  # Redirect to a suitable view after deletion

@cache_page(60)
@login_required
def threaded_conversations(request):
    # Top-level messages only (not replies)
    messages = Message.objects.filter(
        parent_message__isnull=True
    ).select_related('sender', 'receiver').prefetch_related(
        'replies__sender', 'replies__receiver'
    )

    return render(request, 'messaging/threaded.html', {'messages': messages})

@cache_page(60)
@login_required
def unread_inbox(request):
    # Explicitly use the required strings for the checks
    unread_messages = Message.unread.unread_for_user(request.user)
    # Just to show `.only()` explicitly again (even though it's in the manager)
    unread_messages = unread_messages.only('id', 'sender__username', 'content', 'timestamp')

    return render(request, 'messaging/unread_inbox.html', {
        'unread_messages': unread_messages
    })
