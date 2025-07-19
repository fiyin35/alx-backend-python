from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q # For complex lookups
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer


class ConversationViewSet(viewsets.ModelViewSet): 
    """
    A ViewSet for listing, retrieving, and creating conversations.
    Users can only see conversations they are a part of. 
    """

    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated] # only authenticated users can have access

    def get_queryset(self):
         
         """
         Filters conversations to only show those where the requesting user is a participant.
         """
         user = self.request.user

         return Conversation.objects.filter(participants=user).distinct()
    def create(self, request, *args, **kwargs):
         """
        Creates a new conversation.
        Expects 'participants_ids' in the request data, which should be a list of user UUIDs.
        The requesting user is automatically added as a participant.
        """
         participants_ids = request.data.get('participants_ids')

         if request.user.user_id not in participants_ids:
              participants_ids.append(str(request.user.user_id))


         if len(participants_ids) < 2:
              return Response({"detail": "A conversation must have at least two participants (including yourself)"}, status=status.HTTP_400_BAD_REQUEST)

         serializer = self.get_serializer(data={'participants_ids': participants_ids})
         serializer.is_valid(raise_exception=True)
         self.perform_create(serializer)
         
         headers = self.get_success_headers(serializer.data)
         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    


class MessageViewSet(viewsets.ModelViewSet):
     queryset = Message.objects.all()
     serializer_class = MessageSerializer
     permission_classes = [IsAuthenticated]

     def get_queryset(self):
          conversation_id = self.kwargs.get('conversation_conversation_id')
          user = self.request.user

          if not conversation_id:
               return Message.objects.none()
          
          try:
               conversation = Conversation.objects.get(conversation_id=conversation_id)
               if not conversation.participants.filter(user_id=user.user_id).exists():
                    return Message.objects.none()
          except Conversation.DoesNotExist:
               return Message.objects.none()
          
          return Message.objects.filter(conversation=conversation).order_by('sent_at')
     

     def create(self, serializer):
          conversation_id = self.kwargs.get('conversation_conversation_id')
          try:
               conversation = Conversation.objects.get(conversation_id=conversation_id)

               if not conversation.participants.filter(user_id=self.request.user.user_id).exists():
                    raise serializer.ValidationError("You are not a participant in this conversation and cannot send messages to it.")
               serializer.save(sender=self.request.user, conversation=conversation)
          except Conversation.DoesNotExist:
            raise serializer.ValidationError("Conversation not found.")

         
