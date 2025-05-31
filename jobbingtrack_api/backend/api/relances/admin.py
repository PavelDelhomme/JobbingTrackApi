from django.contrib import admin
from .models import Relance, RelanceContact

@admin.register(Relance)
class RelanceAdmin(admin.ModelAdmin):
    list_display = ("id", "candidature_id", "entreprise_id", "date", "status")
    search_fields = ("message", "status")
    list_filter = ("status",)

@admin.register(RelanceContact)
class RelanceContactAdmin(admin.ModelAdmin):
    list_display = ("relance_id", "contact_id")
