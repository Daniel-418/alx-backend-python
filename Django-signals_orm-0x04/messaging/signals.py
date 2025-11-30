from typing import Any, Type
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def notification(sender, instance, created, **kwargs):
    print("notification signal fired")
    if created:
        notification = Notification.objects.create(
            message=instance, user=instance.receiver
        )


@receiver(pre_save, sender=Message)
def log_edits(sender: Type[Message], instance: Message, **kwargs: Any):
    try:
        current_version = Message.objects.get(pk=instance.message_id)
    except Message.DoesNotExist:
        return

    if current_version.content != instance.content:
        MessageHistory.objects.create(
            message=instance, old_content=current_version.content
        )

    instance.edited = True
