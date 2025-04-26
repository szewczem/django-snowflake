from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms
import re

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email", "phone_number", "password1", "password2",)
        
    # Validate email is unique
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    # Validate phone number only digits (and 9 digits long)
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not phone:
            raise forms.ValidationError("Phone number is required.")
        
        if phone.country_code != 48 or len(str(phone.national_number)) != 9:
            raise forms.ValidationError("Enter a valid 9-digit Polish phone number.")

        return phone

    # (Optional) Username validations
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise forms.ValidationError("Username must be at least 3 characters long.")
        return username


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email", "phone_number",)


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Email",)

    class Meta:
        model = CustomUser
        fields = ("username", "password")
