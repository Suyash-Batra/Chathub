import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        self.user = self.scope['user']
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        if self.user.is_authenticated:
            await self.add_participant_to_db()

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '')
        audio_url = data.get('audio_url', None)
        file_url = data.get('file_url', None)
        is_image = data.get('is_image', False)
        msg_id = data.get('id', None)

        if self.user.is_authenticated:
            if not audio_url and not file_url and message.strip() != '':
                new_msg = await self.save_message(message)
                msg_id = new_msg.id

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'audio_url': audio_url,
                'file_url': file_url,
                'is_image': is_image,
                'user': self.user.username,
                'user_id': self.user.id,
                'msg_id': msg_id
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'audio_url': event['audio_url'],
            'file_url': event['file_url'],
            'is_image': event['is_image'],
            'user': event['user'],
            'user_id': event['user_id'],
            'id': event['msg_id']
        }))

    @database_sync_to_async
    def add_participant_to_db(self):
        room = Room.objects.get(id=self.room_id)
        if self.user not in room.participants.all():
            room.participants.add(self.user)

    @database_sync_to_async
    def save_message(self, body):
        room = Room.objects.get(id=self.room_id)
        return Message.objects.create(user=self.user, room=room, body=body)