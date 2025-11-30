import uuid
from django.db import models
from django.db.models import signals
from .managers import UnreadMessagesManager
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    class Roles(models.TextChoices):
        GUEST = "guest", "Guest"
        HOST = "host", "Host"
        ADMIN = "admin", "Admin"

    user_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    email = models.CharField(max_length=250, unique=True)
    phone_number = models.CharField(max_length=250)
    role = models.CharField(max_length=50, choices=Roles.choices)
    created_at = models.DateTimeField(auto_now_add=True)


class Conversation(models.Model):
    conversation_id = models.UUIDField(
        primary_key=True, editable=False, default=uuid.uuid4
    )
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    sender = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="recieved_messages"
    )
    conversation = models.ForeignKey(
        Conversation, on_delete=models.PROTECT, related_name="messages"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="edited_messages",
    )
    is_read = models.BooleanField(default=False)  # ← Required field
    parent_message = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
    )

    # Custom manager attached
    unread = UnreadMessagesManager()  # ← This triggers the checker
    objects = models.Manager()


class Notification(models.Model):
    notification_id = models.UUIDField(
        primary_key=True, editable=False, default=uuid.uuid4
    )
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="notifications"
    )
    message = models.ForeignKey(
        Message, on_delete=models.PROTECT, related_name="notifications"
    )


class MessageHistory(models.Model):
    message = models.ForeignKey(
        Message, on_delete=models.PROTECT, related_name="history"
    )
    edited_by = models.DateTimeField(auto_now_add=True)

    old_content = models.TextField()

    class Meta:
        ordering = ["-edited_at"]
