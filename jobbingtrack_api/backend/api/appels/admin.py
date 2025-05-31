from django.contrib import admin
from .models import Appel

@admin.register(Appel)
class AppelAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "subject", "date_time")
    search_fields = ("subject",)
    list_filter = ("date_time",)
