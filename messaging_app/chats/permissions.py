from rest_framework import permissions


class IsOwnerOrReadOnly(permissions):
    """
    Allow only owners of an object to access/modify it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsConversationParticipant(permissions):
    """
    Allow only participants to view or interact with a conversation.
    """
    def has_object_permission(self, request, view, obj):
        return request.user in [obj.sender, obj.receiver]
