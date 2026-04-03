from celery import shared_task
from django.utils import timezone
from .models import Message

@shared_task
def delete_expired_messages():
    deleted_count, _ = Message.objects.filter(
        expires_at__lt=timezone.now()
    ).delete()

    print(f"Deleted {deleted_count} expired messages")