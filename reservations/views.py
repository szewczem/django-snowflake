from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseRedirect, QueryDict
from django.urls import reverse_lazy, reverse

from django.contrib import messages
from django.utils.safestring import mark_safe

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import DeleteView

from django.core.paginator import Paginator
from django.utils import timezone, dateformat, dateparse
from django.db.models import Q

from .forms import ReservationForm
from .models import Equipment, Reservation, Category
from .filters import EquipmentFilter


# equipment_list view
class EquipmentListView(ListView):
    model = Equipment
    template_name = "reservations/equipment_list.html"
    context_object_name = 'equipment_list'
    paginate_by = 8    # Items per page

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

        ### equipment name ###
        if self.is_valid_queryparam(equipment_name_form):
            qs = qs.filter(name__icontains=equipment_name_form)

        ### dates ###
        if start_date_form or end_date_form:          
            start_date_form, end_date_form = self.is_valid_dates()
            qs = qs.filter(Q(reservation__start_date__lte=start_date_form, reservation__end_date__lte=start_date_form) | Q(reservation__start_date__gte=end_date_form, reservation__end_date__gte=end_date_form) | Q(reservation__isnull=True)).distinct()
            
            # qs = qs.filter(~Q(reservation__start_date__lte=end_date_form, reservation__end_date__gte=end_date_form) & Q(reservation__start_date__gte=end_date_form, reservation__end_date__gte=end_date_form)).distinct()
           
            
            qs = qs.filter(~Q(reservation__start_date__lte=start_date_form, reservation__end_date__gte=end_date_form) | Q(reservation__start_date__lte=start_date_form, reservation__end_date__lte=start_date_form)).distinct()
            
           
            qs = qs.filter(~Q(reservation__end_date=start_date_form)).distinct()
            qs = qs.filter(~Q(reservation__end_date=end_date_form)).distinct()
            qs = qs.filter(~Q(reservation__start_date=start_date_form)).distinct()
            qs = qs.filter(~Q(reservation__start_date=end_date_form)).distinct()   

        ### category ###
        if self.is_valid_queryparam(category_form) and category_form != 'All':
            qs = qs.filter(category__name=category_form)

        ### level ###
        if self.is_valid_queryparam(level_form) and level_form != 'All':
            level_form = level_form.lower()
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

        get = self.request.GET.copy()
        if 'page' in get:
            get.pop('page')
        context['query_string'] = get.urlencode()

        context.update({
            'category': category,
            'level': level,
            'min_paginator_number': min_paginator_number,
            'max_paginator_number': max_paginator_number,
            'start_date_form': start_date_form,
            'end_date_form': end_date_form,
        })
        return context
    
    # keeping dates in session, for equipment_detail reservation form
    def get(self, request, *args, **kwargs):
        start_date_form = self.request.GET.get('start_date')
        end_date_form = self.request.GET.get('end_date')
        start_date_form, end_date_form = self.is_valid_dates()

        if start_date_form:
            request.session['start_date'] = start_date_form

        if end_date_form:
            request.session['end_date'] = end_date_form

        return super().get(request, *args, **kwargs)


# equipment_detail view
class EquipmentDetailView(DetailView):
    model = Equipment
    template_name = 'reservations/equipment_detail.html'
    context_object_name = 'equipment'
    form_class = ReservationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'form': kwargs.get('form', ReservationForm()),
            'start_date': self.request.session.get('start_date'),
            'end_date': self.request.session.get('end_date'),
            'username': self.request.user.username,
            'phone_number': self.request.user.phone_number,
        })
        # context['form'] = ReservationForm()        
        # context['form'] = kwargs.get('form', ReservationForm())
        # context['start_date'] = self.request.session.get('start_date')
        # context['end_date'] = self.request.session.get('end_date')
        # context['username'] = self.request.user.username
        # context['phone_number'] = self.request.user.phone_number

        return context
    
    def get_success_url(self):
        return reverse_lazy('reservations:equipment_detail', kwargs={'pk': self.object.pk})
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ReservationForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            reservation_phone_number = form.cleaned_data['reservation_phone_number']    
            user = request.user  
            try:
                equipment = Equipment.objects.get(id=self.object.id)
            except Equipment.DoesNotExist:
                raise Http404("Equipment does not exist")
            if not equipment.is_reserved(start_date, end_date):
                reservation = Reservation.objects.create(equipment=self.object, user=user, reservation_phone_number=reservation_phone_number, start_date=start_date, end_date=end_date)
                messages.success(request, mark_safe(f"<strong>Success!</strong> Reservation { equipment.category } - { equipment.name }, { reservation.start_date } - { reservation.end_date } accepted."))
            else:                
                messages.error(request, mark_safe("<strong>Holy guacamole!</strong> This equipment is already reserved for the selected dates.")) 
            return HttpResponseRedirect(self.get_success_url())
        else:            
            context = self.get_context_data(form=form)
            return self.render_to_response(context)



# def reserve(request, equipment_id):
#     if request.POST:
#         form = ReservationForm(request.POST)
#         if form.is_valid():
#             start_date = form.cleaned_data["start_date"]
#             end_date = form.cleaned_data["end_date"]
#             user = request.user
#             if user.is_authenticated:        
#                 try:
#                     equipment = Equipment.objects.get(id=equipment_id)
#                 except Equipment.DoesNotExist:
#                     raise Http404("Equipment does not exist")
#                 if not equipment.is_reserved(start_date, end_date):
#                     Reservation.objects.create(equipment=equipment, user=user, start_date=start_date, end_date=end_date)
#                 else:
#                     return HttpResponseForbidden("Nie można zarezerwować, rezerwacja na ten sprzęt już istnieje.")
#                 return redirect('/equipment')
#             else:
#                 return HttpResponseForbidden("Nie jesteś zalogowany")
#         else:
#             return HttpResponseForbidden("Formularz niepoprawnie wypełniony")
#     else:
#         return HttpResponseForbidden("Ten endpoint odpowaida tylko na request POST")
    

class ReservationDeleteView(SuccessMessageMixin, DeleteView):
    model = Reservation
    template_name = 'users/account.html'
    success_url = reverse_lazy('users:account')
    context_object_name = 'reservation'    

    def get_object(self):
        reservation = super().get_object()
        if reservation.user != self.request.user:
            raise Http404('You must be logged in to delete this reservation.')
        return reservation
    
    def get_success_message(self, cleaned_data):
        return f"Reservation: {self.object.equipment.category}, {self.object.equipment.name}, {self.object.start_date} - {self.object.end_date} has been successfully canceled."
