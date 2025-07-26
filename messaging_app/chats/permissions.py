from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions


class IsOwnerOrReadOnly(BasePermission):
    """
    Allow only owners of an object to access/modify it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsConversationParticipant(BasePermission):
    """
    Allow only participants to view or interact with a conversation.
    """
    def has_object_permission(self, request, view, obj):
        return request.user in [obj.sender, obj.receiver]
