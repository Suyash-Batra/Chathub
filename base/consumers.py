import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message
from .tasks import async_generate_image 

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        self.user = self.scope['user']
        try:
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
        except Exception as e:
            print(f"WS Connection Error: {e}")
            await self.close()
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '')
        audio_url = data.get('audio_url')
        file_url = data.get('file_url')
        existing_id = data.get('id')
        if self.user.is_authenticated:
            if existing_id:
                msg_id = existing_id
            elif message.startswith('/generate '):
                prompt_text = message.replace('/generate ', '').strip()
                status_text = f"✨ AI is thinking: '{prompt_text}'..."
                new_msg = await self.save_message(status_text)
                msg_id = new_msg.id
                async_generate_image.delay(prompt_text, self.room_id, self.user.id, msg_id)
                message = status_text
            else:
                new_msg = await self.save_message(message)
                msg_id = new_msg.id
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user': self.user.username,
                    'user_id': self.user.id,
                    'audio_url': audio_url,
                    'file_url': file_url,
                    'msg_id': msg_id,
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def save_message(self, body):
        room = Room.objects.get(id=self.room_id)
        return Message.objects.create(user=self.user, room=room, body=body)