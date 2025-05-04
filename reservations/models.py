from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import Q
from django.db.models import Exists, OuterRef
from django.conf import settings
import urllib.parse


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    

class Equipment(models.Model):   
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    LENGTH_CHOICES = [
        ('130', '130 cm'),
        ('135', '135 cm'),
        ('140', '140 cm'),
        ('145', '145 cm'),
        ('150', '150 cm'),
        ('155', '155 cm'),
        ('160', '160 cm'),
        ('165', '165 cm'),
        ('170', '170 cm'),
        ('175', '175 cm'),
        ('180', '180 cm'),
        ('185', '185 cm'),
    ]

    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='category')
    name = models.CharField(max_length=64)
    length = models.CharField(max_length=3, choices=LENGTH_CHOICES, null=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, null=True)
    banner = models.ImageField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    def get_banner_url(self):
        if self.banner and hasattr(self.banner, 'url'):
            url = self.banner.url
            if url.startswith(settings.MEDIA_URL) and '%3A' in url:
                # Remove the MEDIA_URL prefix
                encoded_url = url[len(settings.MEDIA_URL):]                
                decoded_url = urllib.parse.unquote(encoded_url)
                # decoded_url = decoded_url[:7] + "/" + decoded_url[7:]
                url = decoded_url                
            if url.startswith('https:/') and not url.startswith('https://'):
                url = url.replace('https:/', 'https://')
                # return decoded_url
            return url
        if settings.DEBUG:
            return settings.MEDIA_URL + "equipment_photo/test.jpg"
        return "https://res.cloudinary.com/defosob6j/image/upload/v1746303420/static_images/equipment_photo/test.jpg"
       
    def is_reserved(self, start_date, end_date):
        reservations = self.reservation.all()
        return reservations.filter(start_date__lte=end_date, end_date__gte=start_date).exists()
    
    @classmethod
    def all_not_reserved(cls, start_date_form, end_date_form):
        # # Filter out equipment with overlapping reservations
        # qs = cls.objects.all()

        # # Free equipment
        # qs = qs.filter(
        #     Q(reservation__start_date__lte=start_date_form, reservation__end_date__lte=start_date_form) |
        #     Q(reservation__start_date__gte=end_date_form, reservation__end_date__gte=end_date_form) |      
        #     Q(reservation__isnull=True)
        # ).distinct()

        # # reservation inner and before/afetr
        # qs = qs.filter(
        #     ~Q(reservation__start_date__gte=start_date_form, reservation__end_date__lte=end_date_form) |
        #     Q(reservation__start_date__lte=start_date_form, reservation__end_date__lte=start_date_form)
        # ).distinct()

        # qs = qs.filter(
        #     ~Q(reservation__start_date__gte=start_date_form, reservation__end_date__lte=end_date_form) |
        #     Q(reservation__start_date__gte=end_date_form, reservation__end_date__gte=end_date_form)
        # ).distinct()

        # #  reservation outter and before/afetr
        # qs = qs.filter(
        #     ~Q(reservation__start_date__lte=start_date_form, reservation__end_date__gte=end_date_form)|
        #     Q(reservation__start_date__lte=start_date_form, reservation__end_date__lte=start_date_form)
        # ).distinct()  

        # qs = qs.filter(
        #     ~Q(reservation__start_date__lte=start_date_form, reservation__end_date__gte=end_date_form)|
        #     Q(reservation__start_date__gte=end_date_form, reservation__end_date__gte=end_date_form)
        # ).distinct()       

        # # Exclude with the same starting/ending point
        # qs = qs.filter(~Q(reservation__end_date=start_date_form)).distinct()
        # qs = qs.filter(~Q(reservation__end_date=end_date_form)).distinct()
        # qs = qs.filter(~Q(reservation__start_date=start_date_form)).distinct()
        # qs = qs.filter(~Q(reservation__start_date=end_date_form)).distinct()

        # return qs
        
        overlapping_reservations = Reservation.objects.filter(equipment=OuterRef('pk'), start_date__lte=end_date_form, end_date__gte=start_date_form, is_cancelled=False)
    
        return cls.objects.annotate(has_overlap=Exists(overlapping_reservations)).filter(has_overlap=False)
    

class Reservation(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.PROTECT, related_name='reservation')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservation')
    reservation_phone_number = PhoneNumberField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f'Reservation id: {self.id}, equipment: {self.equipment.category} - {self.equipment.name}'
    
    def cancel(self):
        self.is_cancelled = True
        self.save()


