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
