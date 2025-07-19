from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating conversations.
    Only returns conversations the current user is a participant of.
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user).prefetch_related('participants', 'messages')

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get('participants')
        if not participant_ids:
            raise ValidationError({'participants': 'This field is required.'})

        # Include the current user in the participants list
        conversation = Conversation.objects.create()
        conversation.participants.set(participant_ids + [request.user.id])
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating messages.
    Accepts conversation ID as query param for listing.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.request.query_params.get('conversation')
        if not conversation_id:
            return Message.objects.none()

        conversation = Conversation.objects.filter(id=conversation_id, participants=self.request.user).first()
        if not conversation:
            raise PermissionDenied('You are not a participant in this conversation.')

        return conversation.messages.select_related('sender')

    def perform_create(self, serializer):
        conversation_id = self.request.data.get('conversation')
        if not conversation_id:
            raise ValidationError({'conversation': 'This field is required.'})

        conversation = Conversation.objects.filter(id=conversation_id, participants=self.request.user).first()
        if not conversation:
            raise PermissionDenied('You are not a participant in this conversation.')

        serializer.save(sender=self.request.user, conversation=conversation)
