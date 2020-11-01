from django.forms import ModelForm
from .models import User, Profile
from django.contrib.auth.forms import UserCreationForm


class Profileform(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)


class SingUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
