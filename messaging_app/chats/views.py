from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.status import HTTP_403_FORBIDDEN
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsOwnerOrReadOnly


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['conversation']
    ordering_fields = ['timestamp']

    def get_queryset(self):
        return Message.objects.filter(
            conversation__participants=self.request.user
        ).select_related('sender', 'conversation')

    def perform_create(self, serializer):
        conversation_id = self.request.data.get('conversation')
        if not conversation_id:
            raise ValidationError({'conversation': 'This field is required.'})

        conversation = Conversation.objects.filter(
            id=conversation_id,
            participants=self.request.user
        ).first()

        if not conversation:
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=HTTP_403_FORBIDDEN
            )

        serializer.save(sender=self.request.user, conversation=conversation)
