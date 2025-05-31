from django.contrib import admin
from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "email", "phone", "position")
    search_fields = ("first_name", "last_name", "email", "phone")
