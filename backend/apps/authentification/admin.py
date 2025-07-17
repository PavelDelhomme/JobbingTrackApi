from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from .models import User, UserPermissions


@admin.register(User)
class UserAdmin(BaseAdmin):
    list_display = ('email', 'is_staff', 'is_active', 'date_joined')
    ordering     = ('-date_joined',)
    fieldsets    = (
        (None,               {'fields': ('email', 'password')}),
        ('Informations',     {'fields': ('first_name', 'last_name')}),
        ('Permissions',      {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Dates',            {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )
    search_fields = ('email',)


@admin.register(UserPermissions)
class UserPermissionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter  = ('role',)
    search_fields = ('user__email',)