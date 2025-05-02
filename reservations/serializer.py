from .models import Category, Equipment, Reservation
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('__all__')

class EquipmentSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Equipment
        fields = ('__all__')

class ReservationSerializer(serializers.ModelSerializer):    
    id = serializers.ReadOnlyField()
    class Meta:
        model = Reservation
        fields = ('__all__')


