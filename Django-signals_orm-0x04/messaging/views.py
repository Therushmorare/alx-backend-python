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
