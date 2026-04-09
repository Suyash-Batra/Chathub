import langid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from encrypted_model_fields.fields import EncryptedTextField
from datetime import timedelta
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
from textblob import TextBlob
from django.db.models import Avg

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
    language = models.CharField(max_length=5, default='en', null=True, blank=True)
    current_sentiment = models.FloatField(default=0.0)
    
    def update_vibe(self):
        avg = self.message_set.aggregate(Avg('sentiment_score'))['sentiment_score__avg']
        new_sentiment = avg if avg is not None else 0.0
        Room.objects.filter(id=self.id).update(current_sentiment=new_sentiment)
        self.current_sentiment = new_sentiment
        
    @property
    def vibe_display(self):
        if self.current_sentiment > 0.4:
            return "🔥", "Active Collaboration"
        elif self.current_sentiment > 0.1:
            return "😊", "Steady Discussion"
        elif self.current_sentiment < -0.2:
            return "🧐", "Critical"
        else:
            return "☕", "Neutral / Quiet"
    
    def save(self, *args, **kwargs):
        if self.description and len(self.description) > 10:
            try:
                self.language = langid.classify(self.description)[0]
            except:
                self.language = 'en'
        super().save(*args, **kwargs)
        if self.host:
            try:
                from .utils import check_badges
                check_badges(self.host)
            except Exception as e:
                print(f"Badge Error: {e}")
        
    def delete(self, *args, **kwargs):
        host = self.host # Capture host before deleting
        super().delete(*args, **kwargs)
        from .utils import check_badges
        check_badges(host) # Re-check after room is gone
    
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
    is_ai_generated = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    sentiment_score = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        if self.room.is_ephemeral and not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=24)
        if self.body:
            try:
                text_content = str(self.body)
                analysis = TextBlob(text_content)
                self.sentiment_score = analysis.sentiment.polarity
            except Exception as e:
                print(f"Sentiment Error: {e}")
                self.sentiment_score = 0.0
        else:
            self.sentiment_score = 0.0
        super().save(*args, **kwargs)
        if self.room:
            self.room.participants.add(self.user)
            if self.room.id:
                self.room.update_vibe()
        try:
            from .utils import check_badges
            check_badges(self.user)
        except:
            pass
        
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
            
class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.ImageField(upload_to='badges/', default='badges/default.png')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'badge')

    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"
