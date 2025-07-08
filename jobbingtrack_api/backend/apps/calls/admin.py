#backend/backend/apps/calls/admin.py
from django.contrib import admin
from .models import Call
from api.common.models import UserCall, CompanyCall, ApplicationCall, ContactCall, FollowUpCall

@admin.register(Call)
class CallAdmin(admin.ModelAdmin):
    list_display = ("id", "get_user", "subject", "get_application", "get_company", "get_contact", "get_followup", "date")
    search_fields = ("subject",)
    list_filter = ("date",)

    def get_user(self, obj):
        relation = UserCall.objects.filter(call_id=obj.id).first()
        return relation.user_id if relation else None
    get_user.short_description = 'User'

    def get_company(self, obj):
        relation = CompanyCall.objects.filter(call_id=obj.id).first()
        return relation.entreprise_id if relation else None
    get_company.short_description = 'Company'

    def get_contact(self, obj):
        relation = ContactCall.objects.filter(call_id=obj.id).first()
        return relation.contact_id if relation else None
    get_contact.short_description = 'Contact'

    def get_application(self, obj):
        relation = ApplicationCall.objects.filter(call_id=obj.id).first()
        return relation.application_id if relation else None
    get_application.short_description = 'Application'

    def get_followup(self, obj):
        relation = FollowUpCall.objects.filter(appel_id=obj.id).first()
        return relation.relance_id if relation else None
    get_followup.short_description = 'Follow-up'
