from .models import Badge, UserBadge, Room, Message
from django.contrib.auth.models import User
from django.utils import timezone

def check_badges(user):
    if Room.objects.filter(host=user).count() >= 5:
        award_badge(user, 'Architect')

    current_hour = timezone.now().hour
    if 0 <= current_hour <= 4:
        if Message.objects.filter(user=user).exists():
            award_badge(user, 'Night-Owl')

    ai_message_count = Message.objects.filter(user=user, is_ai_generated=True).count()
    if ai_message_count >= 10:
        award_badge(user, 'Digital-Da-Vinci')
        
    has_text = Message.objects.filter(
    user=user,
    audio_file='', 
    message_file='',
    is_image=False
    ).exclude(body__isnull=True).exists()
    has_image = Message.objects.filter(
        user=user, 
        is_image=True
    ).exists()
    has_file = Message.objects.filter(
        user=user, 
        message_file__isnull=False, 
        is_image=False
    ).exists()
    has_voice = Message.objects.filter(
        user=user,
        audio_file__isnull=False
    ).exists()
    
    if has_text and has_image and has_file and has_voice:
        award_badge(user, 'Multimedia-Master')
        
    external_rooms_count = Message.objects.filter(user=user)\
        .exclude(room__host=user)\
        .values('room')\
        .distinct()\
        .count()

    if external_rooms_count >= 5:
        award_badge(user, 'Conversation-Starter')
        
    if user.is_superuser == True:
        award_badge(user, 'Super-User')

    
    

def award_badge(user, badge_slug):
    try:
        badge = Badge.objects.get(slug=badge_slug)
        UserBadge.objects.get_or_create(user=user, badge=badge)
    except Badge.DoesNotExist:
        pass