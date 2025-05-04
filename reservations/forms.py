from django.forms import ModelForm, widgets
from .models import Reservation, Equipment
from django import forms
from django.contrib import admin
from phonenumber_field.formfields import PhoneNumberField

from urllib.request import urlopen
from django.core.files import File
from tempfile import NamedTemporaryFile
import os


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
            try:
                # Download the image from the URL
                response = urlopen(url, timeout=15)
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(response.read())
                img_temp.flush()

                # Use the filename from the URL
                file_name = os.path.basename(url)
                instance.banner.save(file_name, File(img_temp), save=False)

            except Exception as e:
                raise forms.ValidationError(f"Could not fetch image from URL: {e}")

        if commit:
            instance.save()
        return instance

class ReservationForm(ModelForm):    
     
    class Meta:
        model = Reservation
        fields = ["reservation_phone_number", "start_date", "end_date"]
