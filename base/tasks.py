import requests
import urllib.parse
from celery import shared_task
from django.utils import timezone
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from .models import Message, Room
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import time

@shared_task(bind=True, max_retries=2)
def async_generate_image(self, prompt_text, room_id, user_id, placeholder_id=None):
    channel_layer = get_channel_layer()
    time.sleep(3)
    try:
        encoded_prompt = urllib.parse.quote(prompt_text)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        response = requests.get(url, timeout=300, verify=False)
        if response.status_code == 200:
            image_name = f"ai_{user_id}_{timezone.now().strftime('%Y%m%d%H%M%S')}.png"
            image_file = ContentFile(response.content, name=image_name)
            msg = Message.objects.filter(id=placeholder_id).first()
            if not msg:
                room = Room.objects.get(id=room_id)
                user = User.objects.get(id=user_id)
                msg = Message.objects.create(user=user, room=room)
            msg.body = f"Generated: {prompt_text}"
            msg.message_file = image_file
            msg.is_image = True
            msg.is_ai_generated = True
            msg.save()
            async_to_sync(channel_layer.group_send)(
                f"chat_{room_id}",
                {
                    "type": "chat_message",
                    "message": msg.body,
                    "file_url": msg.message_file.url,
                    "is_image": True,
                    "user": msg.user.username,
                    "msg_id": msg.id,
                    "is_ready": True
                }
            )
        else:
            raise self.retry(countdown=15)
    except Exception as e:
        if self.request.retries >= self.max_retries:
            handle_task_failure(placeholder_id, room_id, str(e))
        else:
            raise self.retry(exc=e, countdown=10)

    return "Success"

def handle_task_failure(placeholder_id, room_id, error_msg):
    channel_layer = get_channel_layer()
    msg = Message.objects.filter(id=placeholder_id).first()
    error_text = "⚠️ AI Service is currently unavailable."
    
    if msg:
        msg.body = error_text
        msg.save()

    async_to_sync(channel_layer.group_send)(
        f"chat_{room_id}",
        {
            "type": "chat_message",
            "message": error_text,
            "is_ready": True,
            "msg_id": placeholder_id,
            "user": "AI"
        }
    )


@shared_task(bind=True, max_retries=1)
def async_get_advice(self, room_id, user_id):
    channel_layer = get_channel_layer()
    try:
        response = requests.get('https://api.adviceslip.com/advice', timeout=10)
        if response.status_code == 200:
            advice_text = response.json()['slip']['advice']
            room = Room.objects.get(id=room_id)
            user = User.objects.get(id=user_id)
            msg = Message.objects.create(
                user=user,
                room=room,
                body=f"Advice 💡: {advice_text}",
                is_ai_generated=False
            )
            async_to_sync(channel_layer.group_send)(
                f"chat_{room_id}",
                {
                    "type": "chat_message",
                    "message": msg.body,
                    "user": msg.user.username,
                    "msg_id": msg.id,
                    "is_ready": True
                }
            )
        else:
            raise self.retry(countdown=5)
    except Exception as e:
        handle_task_failure(None, room_id, str(e))
    return "Advice delivered"

@shared_task(bind=True, max_retries=1)
def async_get_joke(self, room_id, user_id):
    channel_layer = get_channel_layer()
    try:
        response = requests.get('https://icanhazdadjoke.com/slack', timeout=10)
        if response.status_code == 200:
            joke_text = response.json()['attachments'][0]['text']
            room = Room.objects.get(id=room_id)
            user = User.objects.get(id=user_id)
            msg = Message.objects.create(
                user=user,
                room=room,
                body=f"Joke : {joke_text}",
                is_ai_generated=False
            )
            async_to_sync(channel_layer.group_send)(
                f"chat_{room_id}",
                {
                    "type": "chat_message",
                    "message": msg.body,
                    "user": msg.user.username,
                    "msg_id": msg.id,
                    "is_ready": True
                }
            )
        else:
            raise self.retry(countdown=5)
    except Exception as e:
        handle_task_failure(None, room_id, str(e))
    return "Joke delivered"

@shared_task
def delete_expired_messages():
    expired_msgs = Message.objects.filter(
        expires_at__lte=timezone.now()
    )
    count = expired_msgs.count()
    expired_msgs.delete()
    return f"Cleanup complete. Removed {count} expired messages."