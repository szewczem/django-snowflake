from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.core.paginator import Paginator
from django.utils import timezone, dateformat, dateparse
from django.db.models import Q

from .forms import ReservationForm
from .models import Equipment, Reservation, Category
from .filters import EquipmentFilter


# equipment_list view
class EquipmentListView(ListView):
    model = Equipment
    template_name = "equipment_list.html"
    context_object_name = 'equipment_list'
    paginate_by = 8  # Items per page

    def is_valid_queryparam(self, param):
        return param != '' and param is not None
    
    def is_valid_dates(self):
        start_date_form = self.request.GET.get('start_date')
        end_date_form = self.request.GET.get('end_date')
        
        if not self.is_valid_queryparam(end_date_form) and self.is_valid_queryparam(start_date_form): 
            end_date_form = start_date_form
        elif not self.is_valid_queryparam(start_date_form) and self.is_valid_queryparam(end_date_form):
            start_date_form = dateformat.format(timezone.now().date(), 'Y-m-d')
        elif self.is_valid_queryparam(start_date_form) and self.is_valid_queryparam(end_date_form) and start_date_form > end_date_form:    
            start_date_form, end_date_form = end_date_form, start_date_form

        return start_date_form, end_date_form

    def get_queryset(self):
        qs = super().get_queryset()    # qs = Equipment.objects.all()
                
        equipment_name_form = self.request.GET.get('equipment_name')
        start_date_form = self.request.GET.get('start_date')
        end_date_form = self.request.GET.get('end_date')
        category_form = self.request.GET.get('category')
        level_form = self.request.GET.get('level')

        if start_date_form:            
            start_date_form, end_date_form = self.is_valid_dates()
            qs = qs.filter(~Q(reservation__start_date__lte=start_date_form, reservation__end_date__gte=end_date_form) | Q(reservation__start_date__gt=start_date_form, reservation__end_date__gt=end_date_form)).distinct()
            qs = qs.filter(~Q(reservation__end_date=start_date_form)).distinct()
            qs = qs.filter(~Q(reservation__start_date=start_date_form)).distinct()
        elif end_date_form:
            start_date_form, end_date_form = self.is_valid_dates()
            qs = qs.filter(~Q(reservation__start_date__lte=start_date_form, reservation__end_date__gte=start_date_form) & ~Q(reservation__start_date__lte=end_date_form, reservation__end_date__gte=end_date_form)).distinct()

        if self.is_valid_queryparam(equipment_name_form):
            qs = qs.filter(name__icontains=equipment_name_form)

        if self.is_valid_queryparam(category_form) and category_form != 'All':
            qs = qs.filter(category__name=category_form)

        if self.is_valid_queryparam(level_form) and level_form != 'All':
            qs = qs.filter(level=level_form)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        category = Category.objects.values_list('name', flat=True)
        level = Equipment.objects.values_list('level', flat=True).distinct()
        start_date_form, end_date_form = self.is_valid_dates()
        
        page_obj = context['page_obj']
        paginator_limit = 3
        min_paginator_number = max(page_obj.number - paginator_limit, 1)
        max_paginator_number = min(page_obj.number + paginator_limit, page_obj.paginator.num_pages)

        context.update({
            'category': category,
            'level': level,
            'min_paginator_number': min_paginator_number,
            'max_paginator_number': max_paginator_number,
            'start_date_form': start_date_form,
            'end_date_form': end_date_form,
        })
        return context
    

# equipment_detail view
class EquipmentDetailView(DetailView):
    model = Equipment
    template_name = 'equipment_detail.html'
    context_object_name = 'equipment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReservationForm()
        return context


def reserve(request, equipment_id):
    if request.POST:
        form = ReservationForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]
            user = request.user
            if user.is_authenticated:        
                try:
                    equipment = Equipment.objects.get(id=equipment_id)
                except Equipment.DoesNotExist:
                    raise Http404("Equipment does not exist")
                if not equipment.is_reserved(start_date, end_date):
                    Reservation.objects.create(equipment=equipment, user=user, start_date=start_date, end_date=end_date)
                else:
                    return HttpResponseForbidden("Nie można zarezerwować, rezerwacja na ten sprzęt już istnieje.")
                return redirect('/equipment')
            else:
                return HttpResponseForbidden("Nie jesteś zalogowany")
        else:
            return HttpResponseForbidden("Formularz niepoprawnie wypełniony")
    else:
        return HttpResponseForbidden("Ten endpoint odpowaida tylko na request POST")