from django.contrib import admin
from .models import CustomUser, Address
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'is_staff']
    search_fields = ['username', 'email', 'role']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('role', 'phone', 'address')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'image', 'role', 'phone', 'address', 'password1', 'password2'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin) 
admin.site.register(Address)
