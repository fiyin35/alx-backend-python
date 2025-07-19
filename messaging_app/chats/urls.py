
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# The API URLs are now determined automatically by the router.
# For messages, we'll use a nested route pattern to associate them with conversations.
urlpatterns = [
    path('', include(router.urls)),
    # Nested route for messages within a specific conversation.
    # This pattern means: /api/v1/conversations/{conversation_id}/messages/
    path('conversations/<uuid:conversation_conversation_id>/messages/',
         MessageViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='conversation-messages-list'),
    path('conversations/<uuid:conversation_conversation_id>/messages/<uuid:pk>/',
         MessageViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='conversation-messages-detail'),
]