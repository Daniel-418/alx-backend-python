from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification


@receiver(post_save, sender=Message)
def notification(sender, instance, created, **kwargs):
    if created:
        notification = Notification.objects.create(
            message=instance, user=instance.receiver
        )
