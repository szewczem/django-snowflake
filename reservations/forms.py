from django.forms import ModelForm, widgets
from .models import Reservation
from django import forms

class ReservationForm(ModelForm):    
    class Meta:
        model = Reservation
        fields = ["start_date","end_date"]
        widgets = {
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'id': 'startDate'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'id': 'endDate'
            }),
        }
