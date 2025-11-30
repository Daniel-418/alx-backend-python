from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Message, Notification


@receiver(post_save, sender=Message)
def notification(sender, instance, created, **kwargs):
    print("notification signal fired")
    if created:
        notification = Notification.objects.create(
            message=instance, user=instance.receiver
        )


@receiver(pre_save, sender=Message)
def log_edits(sender, instance, **kwargs):
    try:
        current_version = Message.objects.get(pk=instance.message_id)
    except Message.DoesNotExist:
        return

    if current_version.content != instance.content:
        history_entry = {
            "previous_content": current_version.content,
            "edited_at": timezone.now().isoformat(),
        }

        if instance.edit_history is None:
            instance.edit_history = []

        instance.edit_history.append(history_entry)
        instance.is_edited = True
