from django.urls import path

from . import views


app_name = 'reservations'

urlpatterns = [
    path('', views.EquipmentListView.as_view(), name='equipment_list'),
    path('<int:pk>', views.EquipmentDetailView.as_view(), name='equipment_detail'),
    path('<int:equipment_id>/reserve', views.reserve, name='reserve'),
]