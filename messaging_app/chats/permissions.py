from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Conversation

class IsOwner(permissions.BasePermission):
    """
    Allows access only to objects owned by the requesting user.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user  # Assumes `user` field in model

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to interact with its messages.
    """

    def has_permission(self, request, view):
        # Allow access only to authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # obj can be either a Message or a Conversation
        conversation = getattr(obj, 'conversation', obj)  # works for both Message and Conversation
        return request.user in conversation.participants.all()
