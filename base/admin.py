from django.contrib import admin

from .models import Room, Topic, Message, Badge, UserBadge

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Badge)
admin.site.register(UserBadge)