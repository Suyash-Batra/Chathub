from django.forms import ModelForm, forms
from .models import Room, Topic
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants', 'current_sentiment']
        
    def save(self, commit=True):
        room = super().save(commit=False)
        if room.key:
            room.key = make_password(room.key)
        if commit:
            room.save()
            self.save_m2m()
        return room
    
    def clean(self):
        cleaned_data = super().clean()
        is_private = cleaned_data.get("private")
        key = cleaned_data.get("key")
        if is_private and not key:
            raise forms.ValidationError("Private rooms require a key")
        return cleaned_data

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['name']
        