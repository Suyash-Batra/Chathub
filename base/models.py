from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from encrypted_model_fields.fields import EncryptedTextField
from datetime import timedelta
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os


class Topic(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null = True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null = True, blank = True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    key = models.CharField(max_length=200, blank=True, null=True)
    private = models.BooleanField(default=False)
    is_ephemeral = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-updated', '-created']
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = EncryptedTextField(null=True)
    audio_file = models.FileField(upload_to='voice_messages/', null=True, blank=True)
    message_file = models.FileField(upload_to='chat-files/', null=True, blank=True)
    is_image = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.room.is_ephemeral and not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)
        
    def __str__(self):
        if self.body:
            return self.body[0:50]
        if self.audio_file:
            return f"Voice Message by {self.user}"
        return f"File by {self.user}"
    
@receiver(post_delete, sender=Message)
def delete_files_on_message_delete(sender, instance, **kwargs):
    audio = getattr(instance, 'audio_file', None)
    msg_file = getattr(instance, 'message_file', None)
    
    for f in [audio, msg_file]:
        if f and hasattr(f, 'path') and os.path.isfile(f.path):
            os.remove(f.path)
    
    
    