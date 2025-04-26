from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import Q
from django.db.models import Exists, OuterRef

class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    

class Equipment(models.Model):   
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='category')
    name = models.CharField(max_length=32)
    length = models.CharField(max_length=3, null=True)
    level = models.CharField(max_length=20, null=True)
    banner = models.ImageField(default="equipment_photo/test.jpg", blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
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

        # # Return only available equipment
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


