from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields = ("username","first_name","email")

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)
