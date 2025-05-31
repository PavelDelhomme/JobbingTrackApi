from django.contrib import admin
from .models import Entretien

@admin.register(Entretien)
class EntretienAdmin(admin.ModelAdmin):
    list_display = ("id", "candidature", "company", "date_time", "style", "type")
    search_fields = ("style", "type", "location")
    list_filter = ("style", "type")
