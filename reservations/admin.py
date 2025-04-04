from django.contrib import admin
from .models import Equipment, Reservation, Category

# Register your models here.

class EquipmentAdmin(admin.ModelAdmin):
    fields = ['id', 'category', 'name', 'length', 'level', 'banner']
    list_display = ['id', 'category', 'name', 'length', 'level', 'banner']
    readonly_fields = ['id']

class ReservationAdmin(admin.ModelAdmin):
    fields = ['id', 'equipment', 'user', 'start_date', 'end_date']
    list_display = ['id', 'equipment', 'user', 'start_date', 'end_date']
    readonly_fields = ['id']

admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Category)