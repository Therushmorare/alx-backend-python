from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Allows access only to objects owned by the requesting user.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user  # Assumes `user` field in model

