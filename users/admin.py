from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomAuthenticationForm
from .models import CustomUser, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Users Profiles"


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username", "phone_number",]
    fieldsets = [(None, {"fields": ("email", "username", "phone_number", "password")}),
                ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
                ("Important dates", {"fields": ("last_login", "date_joined")})]
    inlines = [UserProfileInline]
    search_fields = ("email", "phone_number")
    add_fieldsets = [(None, {"fields": ("username", "email", "phone_number", "password1", "password2", "is_staff")})]

admin.site.login_form = CustomAuthenticationForm
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile)