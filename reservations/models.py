from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    

class Equipment(models.Model):
    # LENGTH = {
    #     '130': '130 cm',
    #     '145': '145 cm',
    #     '150': '150 cm',
    #     '165': '165 cm',
    #     '175': '175 cm',
    # }
    # LEVEL = {
    #     'begginer': 'A',
    #     'intermediate': 'B',
    #     'expert': 'C',
    # }    
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


class Reservation(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.PROTECT, related_name='reservation')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservation')
    reservation_phone_number = PhoneNumberField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'Reservation id: {self.id}, equipment: {self.equipment.category} - {self.equipment.name}'
