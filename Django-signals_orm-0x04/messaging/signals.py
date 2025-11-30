from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification


@receiver(post_save, sender=Message)
def notification(sender, instance, created, **kwargs):
    print("notification signal fired")
    if created:
        notification = Notification.objects.create(
            message=instance, user=instance.receiver
        )

@receiver(pre_save, sender=Message)
def log_edits(sender, instance, created, **kwargs):
