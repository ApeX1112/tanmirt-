from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User , TanmirtPost ,Message , Comment,UserProfile
from django import forms

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [ 'username', 'email', 'password1', 'password2']


class TanmirtPostForm(ModelForm):
    class Meta:

        model=TanmirtPost
        fields=[
            'image',
            'title',
            'description',
            'lost_or_found',
            
        ]

        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'lost_or_found': forms.Select(attrs={'class': 'form-control'}),
        }
    


class MessageForm(ModelForm):
    class Meta:

        model=Message
        fields=[
            'body'
        ]
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Type your message here...',
                'rows': 4,
                'cols': 50
            }),
        }
        labels = {
            'body': '',  
        }


class CommentForm(ModelForm):
    class Meta:

        model=Comment
        fields=[
            'body'
        ]

class ProfileForm(ModelForm):
    class Meta:
        model=UserProfile
        fields=[
            'image',
            
        ]