from django.forms import ModelForm, widgets
from .models import Reservation

class ReservationForm(ModelForm):    
    class Meta:
        model = Reservation
        fields = ["start_date","end_date"]
        widgets = {
            "start_date": widgets.DateInput(attrs={'type': "date"}),
            "end_date": widgets.DateInput(attrs={'type': "date"}),
        }
