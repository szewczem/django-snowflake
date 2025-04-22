from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email", "phone_number", "password1", "password2",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email", "phone_number",)


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Email",)

    class Meta:
        model = CustomUser
        fields = ("email", "password")
