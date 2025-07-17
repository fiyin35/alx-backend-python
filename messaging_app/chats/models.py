# chats/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# 1. User Model
# Extending Django's built-in AbstractUser to allow for future custom fields
# For now, it's a minimal extension, but you can add fields like 'profile_picture', 'bio', etc.
class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    This allows for adding custom fields later without migrating existing user data.
    Example of a custom field (uncomment to use):
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    """
   
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username

# 2. Conversation Model
class Conversation(models.Model):
    """
    Represents a conversation between multiple users.
    Uses a ManyToManyField to link to the User model, allowing multiple participants.
    """
    # Participants in the conversation. A conversation can have multiple users,
    # and a user can be part of multiple conversations.
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations',
        help_text="Users participating in this conversation"
    )
    created_at = models.DateTimeField(auto_now_add=True)
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
    Links to the sender (User) and the conversation it belongs to.
    """
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
    # The content of the message
    content = models.TextField(
        help_text="The text content of the message"
    )
    # Timestamp when the message was sent
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text="The time when the message was sent"
    )
    # Optional: A field to track if the message has been read
    is_read = models.BooleanField(
        default=False,
        help_text="Indicates if the message has been read by all recipients"
    )

    class Meta:
        # Order messages by their timestamp (oldest first)
        ordering = ['timestamp']
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        # A concise string representation for the message
        return f"Message from {self.sender.username} in Conversation {self.conversation.id} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


