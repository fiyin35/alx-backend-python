# chats/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid # Import uuid for UUIDField primary keys

# 1. User Model
# Extending Django's built-in AbstractUser to allow for future custom fields
class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Now includes an explicit UUID primary key 'user_id'.
    Fields like 'email', 'password', 'first_name', 'last_name' are inherited
    directly from AbstractUser and do not need to be redefined here.
    """
    user_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for the user"
    )

    def __str__(self):
        return self.username

# 2. Conversation Model
class Conversation(models.Model):
    """
    Represents a conversation between multiple users.
    Now includes an explicit UUID primary key 'conversation_id'.
    Uses a ManyToManyField to link to the User model, allowing multiple participants.
    """
    conversation_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for the conversation"
    )
    # Participants in the conversation. A conversation can have multiple users,
    # and a user can be part of multiple conversations.
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations',
        help_text="Users participating in this conversation"
    )
    # A field to track when the conversation was created
    created_at = models.DateTimeField(auto_now_add=True)
    # A field to track the last time a message was sent in this conversation
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Order conversations by the most recently updated one
        ordering = ['-updated_at']
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"

    def __str__(self):
        # A more descriptive string representation for the conversation
        # Lists the usernames of the participants
        return f"Conversation with: {', '.join(user.username for user in self.participants.all())}"


# 3. Message Model
class Message(models.Model):
    """
    Represents a single message within a conversation.
    Now includes an explicit UUID primary key 'message_id'.
    Links to the sender (User) and the conversation it belongs to.
    Field names 'content' and 'timestamp' have been updated to 'message_body' and 'sent_at'.
    """
    message_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for the message"
    )
    # The user who sent the message
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        help_text="The user who sent this message"
    )
    # The conversation this message belongs to
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        help_text="The conversation this message is part of"
    )
    # The content of the message, renamed to message_body
    message_body = models.TextField(
        help_text="The text content of the message"
    )
    # Timestamp when the message was sent, renamed to sent_at
    sent_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The time when the message was sent"
    )
    # Optional: A field to track if the message has been read
    is_read = models.BooleanField(
        default=False,
        help_text="Indicates if the message has been read by all recipients"
    )

    class Meta:
        # Order messages by their sent_at (oldest first)
        ordering = ['sent_at']
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        # A concise string representation for the message
        return f"Message from {self.sender.username} in Conversation {self.conversation.id} at {self.sent_at.strftime('%Y-%m-%d %H:%M')}"

