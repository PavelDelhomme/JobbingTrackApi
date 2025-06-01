from django.contrib import admin
from .models import Entretien
from common.models import UserEntretien, CandidatureEntretien, EntrepriseEntretien, ContactEntretien

@admin.register(Entretien)
class EntretienAdmin(admin.ModelAdmin):
    list_display = ("id", "get_user", "get_subject", "get_candidature", "get_company", "get_contact", "date_time")
    search_fields = ("subject",)
    list_filter = ("date_time",)

    def get_user(self, obj):
        relation = UserEntretien.objects.filter(entretien_id=obj.id).first()
        return relation.user_id if relation else None
    get_user.short_description = 'User'

    def get_candidature(self, obj):
        relation = CandidatureEntretien.objects.filter(entretien_id=obj.id).first()
        return relation.candidature_id if relation else None
    get_candidature.short_description = 'Candidature'

    def get_company(self, obj):
        relation = EntrepriseEntretien.objects.filter(entretien_id=obj.id).first()
        return relation.entreprise_id if relation else None
    get_company.short_description = 'Entreprise'

    def get_contact(self, obj):
        relation = ContactEntretien.objects.filter(entretien_id=obj.id).first()
        return relation.contact_id if relation else None
    get_contact.short_description = 'Contact'

    def get_subject(self, obj):
        return obj.title or "Sans titre"
    get_subject.short_description = "Sujet"