from django.shortcuts import render, redirect
from django.contrib.auth import login, logout

from .forms import CustomUserCreationForm, CustomAuthenticationForm

from reservations.models import Reservation

# Create your views here.
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)          
        if form.is_valid():
            login(request, form.save())
            return redirect("reservations:equipment_list")
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', { 'form': form })

def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect("reservations:equipment_list")
    else:
        form = CustomAuthenticationForm(request.POST)
    return render(request, 'users/login.html', { 'form': form })

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/")
    
def account_view(request):
    user_reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'users/account.html', { 'user_reservations': user_reservations})
