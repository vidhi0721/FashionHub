from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "class":"form-control",
        "placeholder":"First Name"
    }))

    username = forms.CharField(widget=forms.TextInput(attrs={
        "class":"form-control",
        "placeholder":"Username"
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class":"form-control",
        "placeholder":"Email"
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class":"form-control",
        "placeholder":"Password"
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class":"form-control",
        "placeholder":"Confirm Password"
    }))

    class Meta:
        model = User
        fields = ["first_name","username","email","password1","password2"]