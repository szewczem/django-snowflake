from django.forms import ModelForm, widgets
from .models import Reservation
from django import forms
from phonenumber_field.formfields import PhoneNumberField

class ReservationForm(ModelForm):    
     
    class Meta:
        model = Reservation
        fields = ["reservation_phone_number", "start_date", "end_date"]
