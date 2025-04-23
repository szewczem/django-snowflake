from django.urls import path

from . import views


app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name="register"),
    path('login/', views.CustomLoginView.as_view(), name="login"),
    path('logout/', views.CustomLogoutView.as_view(), name="logout"),
    path('account/', views.Account.as_view(), name="account"),
]