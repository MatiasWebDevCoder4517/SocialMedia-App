from django import forms
from .models import TalkerProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class TalkerProfileForm(forms.ModelForm):
    class Meta:
        model = TalkerProfile
        fields = ('avatar',)


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email']


class TalkerProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = TalkerProfile
        fields = ['bio', 'avatar']
