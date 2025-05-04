from django.forms import ModelForm, widgets
from .models import Reservation, Equipment
from django import forms


class EquipmentForm(forms.ModelForm):
    banner_url = forms.URLField(required=False, label="Banner URL (Cloudinary)", help_text="If you paste a URL here, we'll use it instead of uploading a file.")

    class Meta:
        model = Equipment
        fields = ['category', 'name', 'length', 'level', 'banner', 'banner_url', 'description']

    def clean(self):
        cleaned = super().clean()
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        url = self.cleaned_data.get('banner_url')

        if url:
            instance.banner = url 

        if commit:
            instance.save()
        return instance

class ReservationForm(ModelForm):    
     
    class Meta:
        model = Reservation
        fields = ["reservation_phone_number", "start_date", "end_date"]
