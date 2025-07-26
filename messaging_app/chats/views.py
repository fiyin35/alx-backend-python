from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsOwnerOrReadOnly

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user).prefetch_related('participants', 'messages')

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get('participants')
        if not participant_ids:
            raise ValidationError({'participants': 'This field is required.'})

        conversation = Conversation.objects.create()
        conversation.participants.set(participant_ids + [request.user.id])
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['conversation']
    ordering_fields = ['timestamp']

    def get_queryset(self):
        queryset = Message.objects.select_related('sender', 'conversation')
        return queryset.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation_id = self.request.data.get('conversation')
        if not conversation_id:
            raise ValidationError({'conversation': 'This field is required.'})

        conversation = Conversation.objects.filter(id=conversation_id, participants=self.request.user).first()
        if not conversation:
            raise PermissionDenied('You are not a participant in this conversation.')

        serializer.save(sender=self.request.user, conversation=conversation)
