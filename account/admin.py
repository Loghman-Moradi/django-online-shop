from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .form import ShopUserCreationForm, ShopUserChangeForm


class AddressInline(admin.TabularInline):
    model = Address
    extra = 1


@admin.register(ShopUser)
class ShopUserAdmin(UserAdmin):
    ordering = ['phone']

    add_form = ShopUserCreationForm
    form = ShopUserChangeForm
    model = ShopUser

    list_display = ['phone', 'first_name', 'last_name', 'is_active', 'is_staff']
    inlines = [AddressInline]

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ("Personal Info", {'fields': ('first_name', 'last_name')}),
        ("Permissions", {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ("Important Dates", {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {'fields': ('phone', 'password1', 'password2')}),
        ("Personal Info", {'fields': ('first_name', 'last_name')}),
        ("Permissions", {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ("Important Dates", {'fields': ('last_login', 'date_joined')}),

    )















