from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# from phonenumber_field.modelfields import PhoneNumberField

class CustomUser(AbstractUser):
    username = models.CharField(max_length=20, unique=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)

    USERNAME_FIELD = 'email'  # Login via email (don't need backeds.py)
    REQUIRED_FIELDS = ['username', 'phone_number'] 

    def __str__(self):
        return self.email
    

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "Users Profiles"