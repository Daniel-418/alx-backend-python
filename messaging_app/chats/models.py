import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


# Create your models here.
class user(AbstractUser):
    class roles(models.TextChoices):
        GUEST = "guest", "Guest"
        HOST = "host", "Host"
        ADMIN = "admin", "Admin"

    user_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.CharField(max_length=250, unique=True)
    password_hash = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=250)
    role = models.CharField(max_length=50, choices=roles.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField(
        Group,
        blank=True,
        help_text=(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        # This is the unique name that fixes the clash
        related_name="chats_user_groups",
        related_query_name="user",
    )

    # 2. Add this 'user_permissions' field
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        help_text="Specific permissions for this user.",
        # This is the other unique name that fixes the clash
        related_name="chats_user_permissions",
        related_query_name="user",
    )


class Conversation(models.Model):
    conversation_id = models.UUIDField(
        primary_key=True, editable=False, default=uuid.uuid4
    )
    participants_id = models.ForeignKey(
        user, on_delete=models.PROTECT, related_name="conversations"
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    sender_id = models.ForeignKey(
        user, on_delete=models.PROTECT, related_name="messages"
    )
    conversation_id = models.ForeignKey(
        Conversation, on_delete=models.PROTECT, related_name="messages"
    )
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
