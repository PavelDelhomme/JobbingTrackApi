#backend/api/entretiens/admin.py
from django.contrib import admin
from .models import Interview
from api.common.models import UserInterview, ApplicationInterview, CompanyInterview, ContactInterview

@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ("id", "get_user", "get_subject", "get_application", "get_company", "get_contact", "date_time")
    search_fields = ("subject",)
    list_filter = ("date_time",)

    def get_user(self, obj):
        relation = UserInterview.objects.filter(interview_id=obj.id).first()
        return relation.user_id if relation else None
    get_user.short_description = 'User'

    def get_application(self, obj):
        relation = ApplicationInterview.objects.filter(interview_id=obj.id).first()
        return relation.application_id if relation else None
    get_application.short_description = 'Application'

    def get_company(self, obj):
        relation = CompanyInterview.objects.filter(interview_id=obj.id).first()
        return relation.company_id if relation else None
    get_company.short_description = 'Company'

    def get_contact(self, obj):
        relation = ContactInterview.objects.filter(interview_id=obj.id).first()
        return relation.contact_id if relation else None
    get_contact.short_description = 'Contact'

    def get_subject(self, obj):
        return obj.title or "Sans titre"
    get_subject.short_description = "Sujet"