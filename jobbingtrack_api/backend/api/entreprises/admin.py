from django.contrib import admin
from .models import Entreprise

@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type", "email", "phone")
    search_fields = ("name", "email")
