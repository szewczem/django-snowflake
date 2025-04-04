import django_filters as df
from .models import Equipment

class EquipmentFilter(df.FilterSet):
    start_date = df.DateFilter('start_date', label=('Start date'))
    end_date = df.DateFilter(field_name='end_date')
    class Meta:
        model = Equipment 
        fields = {
            'category': ['exact'],
            'name': ['contains'],
            'level': ['exact'],
        }

