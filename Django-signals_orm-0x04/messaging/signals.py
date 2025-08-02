from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

# Create a notification when a new message is sent
@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)

# Log previous content before a message is edited
@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        try:
            original = Message.objects.get(pk=instance.pk)
            if original.content != instance.content:
                MessageHistory.objects.create(message=original, old_content=original.content, edited_by=instance.sender)
                instance.edited = True
        except Message.DoesNotExist:
            pass

# Cleanup messages, notifications, and histories when a user is deleted
@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(edited_by=instance).delete()

