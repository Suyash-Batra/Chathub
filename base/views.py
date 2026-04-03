import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.urls import reverse_lazy, reverse
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm, TopicForm
from django.http import JsonResponse

class CreateRoomView(LoginRequiredMixin, CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'base/room_form.html'
    login_url = 'login'

    def form_valid(self, form):
        room = form.save(commit=False)
        room.host = self.request.user
        room.save()
        return redirect('home')

class HomeView(ListView):
    model = Room
    template_name = 'base/home.html'
    context_object_name = 'rooms'

    def get_queryset(self):
        q = self.request.GET.get('q') or ''
        return Room.objects.filter(
            Q(topic__name__icontains=q) |
            Q(name__icontains=q) |
            Q(description__icontains=q)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q') or ''
        rooms = context['rooms']

        context['topics'] = Topic.objects.all()
        context['roomcount'] = rooms.count()
        context['room_messages'] = Message.objects.filter(
            Q(room__topic__name__icontains=q)
        ).order_by('-created')

        return context

class RoomView(View):
    def get(self, request, pk):
        room = Room.objects.get(id=pk)
        if room.private:
            if not request.session.get(f'room_{room.id}_access'):
                return render(request, 'base/room_pass.html', {'room': room})
        context = {
            'room': room,
            'room_messages': room.message_set.all().order_by('created'),
            'participants': room.participants.all()
        }
        return render(request, 'base/room.html', context)

    def post(self, request, pk):
        room = Room.objects.get(id=pk)
        if room.private and not request.session.get(f'room_{room.id}_access'):
            entered_key = request.POST.get('key')
            if not check_password(entered_key, room.key):
                return render(request, 'base/room_pass.html', {
                    'room': room,
                    'error': 'Invalid password'
                })
            request.session[f'room_{room.id}_access'] = True
            return redirect('room', pk=room.id)
        Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    
class UpdateRoomView(LoginRequiredMixin, UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'base/room_form.html'
    login_url = 'login'
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        room = self.get_object()
        if request.user != room.host:
            return HttpResponse('You are not the owner of the room')
        return super().dispatch(request, *args, **kwargs)

class DeleteRoomView(LoginRequiredMixin, DeleteView):
    model = Room
    template_name = 'base/delete.html'
    login_url = 'login'
    success_url = reverse_lazy('home')
    context_object_name = "obj"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context["name"] = obj.name
        return context
    
class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'base/login_register.html', {'page': 'login'})

    def post(self, request):
        username = request.POST.get("username").lower()
        password = request.POST.get("pass")

        try:
            User.objects.get(username=username)
        except:
            messages.error(request, "User dosent exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Wrong username or password")

        return render(request, 'base/login_register.html', {'page': 'login'})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')
    
class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'base/login_register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured while registration')

        return render(request, 'base/login_register.html', {'form': form})

class DeleteMessageView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'base/delete.html'
    login_url = 'login'
    context_object_name = "obj"
    
    def get_success_url(self):
        obj = self.get_object()
        return reverse('room', kwargs={'pk': obj.room.id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context["name"] = obj.body
        return context
    
class UserProfileView(View):
    def get(self, request, pk):
        user = User.objects.get(id=pk)
        rooms = user.room_set.all()

        context = {
            'users': user,
            'rooms': rooms,
            'room_messages': user.message_set.all(),
            'topics': Topic.objects.all(),
            'roomcount': rooms.count()
        }

        return render(request, 'base/profile.html', context)

class UpdateUserView(LoginRequiredMixin, View):
    def get(self, request):
        form = UserForm(instance=request.user)
        return render(request, 'base/update_user.html', {'form': form})

    def post(self, request):
        form = UserForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=request.user.id)

        return render(request, 'base/update_user.html', {'form': form})

class AddTopicView(LoginRequiredMixin, CreateView):
    model = Topic
    form_class = TopicForm
    template_name = 'base/room_form.html'
    login_url = 'login'

    def form_valid(self, form):
        form.save()
        return redirect('home')

class VoiceUploadView(LoginRequiredMixin, View):
    def post(self, request, pk):
        room = get_object_or_404(Room, id=pk)
        audio = request.FILES.get('audio')
        if audio:
            msg = Message.objects.create(user=request.user, room=room, audio_file=audio, body="Voice Message")
            return JsonResponse({'id': msg.id, 'audio_url': msg.audio_file.url, 'user': request.user.username, 'user_id': request.user.id})
        return JsonResponse({'error': 'No audio'}, status=400)

class FileUploadView(LoginRequiredMixin, View):
    def post(self, request, pk):
        try:
            room = get_object_or_404(Room, id=pk)
            file = request.FILES.get('file')
            if not file:
                return JsonResponse({'error': 'No file provided'}, status=400)
            ext = os.path.splitext(file.name)[1].lower()
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
            is_img = ext in valid_extensions
            msg = Message.objects.create(
                user=request.user, 
                room=room, 
                message_file=file, 
                is_image=is_img, 
                body=f"File: {file.name}"
            )

            return JsonResponse({
                'id': msg.id, 
                'file_url': msg.message_file.url, 
                'is_image': is_img, 
                'user': request.user.username, 
                'user_id': request.user.id
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)