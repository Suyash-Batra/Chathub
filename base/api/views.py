from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room, Topic
from .serializers import RoomSerializer, TopicSerializer, UserSerializer
from django.contrib.auth.models import User

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',
        'GET /api/topics',
        'GET /api/topics/:id',
        'GET /api/users',
        'GET /api/users/:id',
    ]
    return Response(routes)
@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializers = RoomSerializer(rooms, many=True)
    return Response(serializers.data)
@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializers = RoomSerializer(room, many=False)
    return Response(serializers.data)
@api_view(['GET'])
def getTopics(request):
    topics = Topic.objects.all()
    serializers = TopicSerializer(topics, many=True)
    return Response(serializers.data)
@api_view(['GET'])
def getUsers(request):
    users = User.objects.all()
    serializers = UserSerializer(users, many=True)
    return Response(serializers.data)
@api_view(['GET'])
def getUser(request, pk):
    user = User.objects.get(id=pk)
    serializers = UserSerializer(user, many=False)
    return Response(serializers.data)
@api_view(['GET'])
def getTopic(request, pk):
    topic = Topic.objects.get(id=pk)
    serializers = TopicSerializer(topic, many=False)
    return Response(serializers.data)