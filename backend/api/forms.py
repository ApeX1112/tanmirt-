from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User , TanmirtPost 

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
            'description'
        ]