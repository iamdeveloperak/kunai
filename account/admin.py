from django.contrib import admin
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
admin.site.unregister(Group)

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm


    fieldsets = (
        ('User info', {'fields': ('username','password')}),
        ('Personal info', {'fields': ('first_name','last_name','email','phone_number')}),
        ('Permissions', {'fields': ('is_staff','is_active','is_premium')}),
        ('Important Dates', {'fields': ('last_login','date_joined')}),
        ('Advance Options', {
            'classes': ('collapse',),
            'fields': ('groups', 'user_permissions'),
        }),

    )
    add_fieldsets = (
        ('User info', {'fields': ('username','password')}),
        ('Personal info', {'fields': ('first_name','last_name','email','phone_number')}),
        ('Permissions', {'fields': ('is_staff','is_active')}),
    )
admin.site.register(CustomUser, CustomUserAdmin)