from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.urls import reverse_lazy, reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.views import View

from .models import CustomUser

from .forms import CustomUserCreationForm, CustomAuthenticationForm

from reservations.models import Reservation

from django.http import JsonResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("reservations:equipment_list")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)
    

class EmailValidationView(View):
    def get(self, request, *args, **kwargs):
        email = request.GET.get('email', '').strip()
        if not email:
            return JsonResponse({'error': 'Email is required.'}, status=400)
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({'error': 'Invalid email format.'}, status=400)
        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({'exists': True})
        return JsonResponse({'exists': False})
    

# def register_view(request):
#     if request.method == "POST":
#         form = CustomUserCreationForm(request.POST)          
#         if form.is_valid():
#             login(request, form.save())
#             return redirect("reservations:equipment_list")
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'users/register.html', { 'form': form })


class CustomLoginView(LoginView):
    template_name = "users/login.html"
    authentication_form = CustomAuthenticationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("reservations:equipment_list")

# def login_view(request):
#     if request.method == "POST":
#         form = CustomAuthenticationForm(data=request.POST)
#         if form.is_valid():
#             login(request, form.get_user())
#             if 'next' in request.POST:
#                 return redirect(request.POST.get('next'))
#             else:
#                 return redirect("reservations:equipment_list")
#     else:
#         form = CustomAuthenticationForm(request.POST)
#     return render(request, 'users/login.html', { 'form': form })


class CustomLogoutView(LogoutView):
    pass

# def logout_view(request):
#     if request.method == "POST":
#         logout(request)
#         return redirect("/")
    

class Account(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = "users/account.html"
    context_object_name = 'user_reservations'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs
    
# def account_view(request):
#     user_reservations = Reservation.objects.filter(user=request.user)
#     return render(request, 'users/account.html', { 'user_reservations': user_reservations})
