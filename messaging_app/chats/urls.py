from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Create a router and register our ConversationViewSet with it.
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# The API URLs are now determined automatically by the router for conversations.
# For messages, we'll use a nested route pattern to associate them with conversations.
urlpatterns = [
    path('', include(router.urls)), # Includes routes like /conversations/ and /conversations/<uuid:pk>/
    # Nested route for messages within a specific conversation.
    # This pattern means: /api/conversations/{conversation_id}/messages/
    # It allows listing messages for a conversation and creating a new message in it.
    path('conversations/<uuid:conversation_conversation_id>/messages/',
         MessageViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='conversation-messages-list'),
    # Nested route for individual messages within a specific conversation.
    # This pattern means: /api/conversations/{conversation_id}/messages/{message_id}/
    # It allows retrieving, updating, and deleting a specific message.
    path('conversations/<uuid:conversation_conversation_id>/messages/<uuid:pk>/',
         MessageViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='conversation-messages-detail'),
]
