from django.contrib import admin
from .models import Application
from api.common.models import CandidatureContact

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "application_date", "contract_type", "application_status")
    search_fields = ("title", "platform", "location")
    list_filter = ("application_status", "contract_type")

@admin.register(ApplicationContact)
class ApplicationContactAdmin(admin.ModelAdmin):
    list_display = ("application_id", "contact_id")
