from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User

from base.models import Room, Topic, UserBadge
from .serializers import RoomSerializer, TopicSerializer, UserSerializer, UbadgeSerializer

class GetRoutes(APIView):
    def get(self, request):
        routes = [
            'GET /api',
            'GET /api/rooms',
            'GET /api/rooms/:id',
            'GET /api/topics',
            'GET /api/topics/:id',
            'GET /api/users',
            'GET /api/users/:id',
            'GET /api/badges/',
            'GET /api/badges/:id',
        ]
        return Response(routes)

class RoomList(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class RoomDetail(generics.RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class TopicList(generics.ListAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class TopicDetail(generics.RetrieveAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class BadgeList(generics.ListAPIView):
    queryset = UserBadge.objects.all()
    serializer_class = UbadgeSerializer
    
class BadgeDetail(generics.RetrieveAPIView):
    queryset = UserBadge.objects.all()
    serializer_class = UbadgeSerializer