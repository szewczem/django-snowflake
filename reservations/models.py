from django.db import models
from django.contrib.auth import get_user_model


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    

class Equipment(models.Model):
    LENGTH = {
        '130': '130 cm',
        '145': '145 cm',
        '150': '150 cm',
        '165': '165 cm',
        '175': '175 cm',
    }
    LEVEL = {
        'begginer': 'A',
        'intermediate': 'B',
        'expert': 'C',
    }    
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='category')
    name = models.CharField(max_length=32)
    length = models.CharField(max_length=3, choices=LENGTH, null=True)
    level = models.CharField(max_length=20, choices=LEVEL, null=True)
    banner = models.ImageField(default="Equipment_photo/test.jpg", blank=True)

    def __str__(self):
        return f'{self.category} - {self.name}'
    
    def is_reserved(self, start_date, end_date):
        reservations = self.reservation.all()
        return reservations.filter(start_date__lte=end_date, end_date__gte=start_date).exists()


class Reservation(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.PROTECT, related_name='reservation')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='reservation')
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'Reservation id: {self.id}, equipment: {self.equipment.category} - {self.equipment.name}'
