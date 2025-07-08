from django.contrib import admin
from .models import FollowUp
from api.common.models import ContactFollowUp, ApplicationFollowUp, CompanyFollowUp

@admin.register(FollowUp)
class FollowUpAdmin(admin.ModelAdmin):
    list_display = ("id", "get_application", "get_company", "date", "status")

    def get_application(self, obj):
        rel = ApplicationFollowUp.objects.filter(followup_id=obj.id).first()
        return rel.application_id if rel else None
    get_application.short_description = "Application"

    def get_company(self, obj):
        rel = CompanyFollowUp.objects.filter(followup_id=obj.id).first()
        return rel.company_id if rel else None
    get_company.short_description = "Company"

@admin.register(ContactFollowUp)
class FollowUpContactAdmin(admin.ModelAdmin):
    list_display = ("followup_id", "contact_id")
