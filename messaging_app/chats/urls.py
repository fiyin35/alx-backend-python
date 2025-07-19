from .views import ConversationViewSet, MessageViewSet
from rest_framework import routers
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

urlpatterns = [
    path('', include(router.urls)), # Includes routes like /conversations/ and /conversations/<uuid:pk>/
    path('conversations/<uuid:conversation_conversation_id>/messages/',
         MessageViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='conversation-messages-list'),
    path('conversations/<uuid:conversation_conversation_id>/messages/<uuid:pk>/',
         MessageViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='conversation-messages-detail'),
]
