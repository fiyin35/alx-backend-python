from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions
from rest_framework.views import Request, View
from .models import Conversation, Message


class IsOwnerOrReadOnly(BasePermission):
    """
    Allow only owners of an object to access/modify it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user



class IsParticipantOfConversation(BasePermission):
    """
    Custom permission:
    - Only authenticated users allowed
    - Only participants in a conversation can send/view/update/delete messages
    """

    def has_permission(self, request: Request, view: View) -> bool:
        # Allow only authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request: Request, view: View, obj) -> bool:
        user = request.user

        # Get the related conversation
        if isinstance(obj, Message):
            conversation = obj.conversation
        elif isinstance(obj, Conversation):
            conversation = obj
        else:
            return False

        is_participant = user == conversation.sender or user == conversation.receiver

        # Restrict to participants for any method
        if request.method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
            return is_participant

        return False



class IsAdmin(BasePermission):
    """
    Permission to only allow admin users.
    """

    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'admin'
        )


class CanManageUsers(BasePermission):
    """
    Permission for user management - only admins can manage users.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        # Admin can do everything
        if request.user.role == 'admin':
            return True

        # Host can only read user data
        if request.user.role == 'host' and request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        # Users can always access their own data
        if obj == request.user:
            return True

        # Admin can access any user
        if request.user.role == 'admin':
            return True

        # Host can only read other user data
        if request.user.role == 'host' and request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        return False
