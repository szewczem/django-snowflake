from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views
from reservations.views import EquipmentViewSet, CategoryViewSet, ReservationViewSet

from rest_framework import routers


router = routers.DefaultRouter()
router.register('equipment', EquipmentViewSet, 'eqquipment')
router.register('category', CategoryViewSet, 'category')
router.register('reservation', ReservationViewSet, 'reservation')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.mainpage),
    path('about/', views.aboutpage),
    path('equipment/', include('reservations.urls')),
    path('users/', include('users.urls')),

    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)