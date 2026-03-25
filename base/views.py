from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic, Message
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RoomForm, UserForm, TopicForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

@login_required(login_url = 'login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit = False)
            room.host = request.user
            room.save()
            return redirect('home')
    context = {'form' : form}
    return render(request, 'base/room_form.html', context)
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains = q) | Q(name__icontains=q) | Q(description__icontains = q))
    topic = Topic.objects.all()
    roomCount = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms': rooms, 'topics': topic, 'roomcount': roomCount, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_participants = room.participants.all()
    room_messages = room.message_set.all().order_by('created')
    if request.method =='POST':
        message = Message.objects.create(
            user=request.user,
            room = room,
            body = request.POST.get('body'),
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'room': room, 'room_messages': room_messages, 'participants': room_participants}
    return render(request,'base/room.html', context)
@login_required(login_url = 'login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse('You are not the owner of the room')
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)
@login_required(login_url = 'login')
def deleteRoom(request, pk):
    room = Room.objects.get(id = pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get("username").lower()
        password = request.POST.get("pass")
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User dosent exist")
        user= authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Wrong username or password")
    context = {'page': page}
    return render(request, 'base/login_register.html', context)
def logoutUser(request):
    logout(request)
    return redirect('home')
def registerUser(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect ('home')
        else:
            messages.error(request, 'An error occured while registration try a different username or check ur password')
    context = {'form': form}
    return render(request, 'base/login_register.html', context)
@login_required(login_url = 'login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message.body})
def userProfile(request, pk):
    users = User.objects.get(id=pk)
    rooms = users.room_set.all()
    roomcount = rooms.count()
    room_messages = users.message_set.all()
    topics = Topic.objects.all()
    context = {'users': users, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics, 'roomcount': roomcount}
    return render(request, 'base/profile.html', context)
@login_required(login_url='login')
def updateUser(request):
    form = UserForm(instance=request.user)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=request.user.id)
    context = {'form': form}
    return render(request, 'base/update_user.html', context)
@login_required(login_url='login')
def addTopic(request):
    form = TopicForm()
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            room = form.save()
            return redirect('home')
    context = {'form' : form}
    return render(request, 'base/room_form.html', context)
    