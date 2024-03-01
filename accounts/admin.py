from django.contrib import admin
from .models import User, ConfirmationToken, OTP, Membership
from django.contrib.auth.admin import UserAdmin

# Register your models here.

admin.site.register(ConfirmationToken)

class UserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('name', 'email', 'phone_number', 'password', 'date_joined', 'last_login')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'phone_number', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'date_joined',)}
        ),
    )
    search_fields = ('name',)
    ordering = ('date_joined',)

admin.site.register(User, UserAdmin)

admin.site.register(OTP)
admin.site.register(Membership)
