import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studybud.settings')

from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from base.consumers import ChatConsumer

application = ProtocolTypeRouter({
    "http": django_asgi_app,

    "websocket": AuthMiddlewareStack(   # ✅ THIS FIXES 'user'
        URLRouter([
            path("ws/chat/<int:room_id>/", ChatConsumer.as_asgi()),
        ])
    ),
})