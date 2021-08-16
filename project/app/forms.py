from django import forms
from django.contrib.auth.models import User
from .models import Profile



class UserUpdateForm(forms.ModelForm):
    first_name = forms.TextInput()
    last_name = forms.TextInput()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']