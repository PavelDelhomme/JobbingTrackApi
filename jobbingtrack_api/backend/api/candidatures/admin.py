from django.contrib import admin
from .models import Candidature, CandidatureContact

@admin.register(Candidature)
class CandidatureAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "candidature_date", "contract_type", "candidature_status")
    search_fields = ("title", "platform", "location")
    list_filter = ("candidature_status", "contract_type")

@admin.register(CandidatureContact)
class CandidatureContactAdmin(admin.ModelAdmin):
    list_display = ("candidature_id", "contact_id")
