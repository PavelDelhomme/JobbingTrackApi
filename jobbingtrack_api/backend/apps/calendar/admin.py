#backend/api/evenements/admin.py
from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "type", "start_date", "end_date")
    search_fields = ("title", "description")
    list_filter = ("type",)
