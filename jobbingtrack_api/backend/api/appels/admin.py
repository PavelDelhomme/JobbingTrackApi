#backend/api/appels/admin.py
from django.contrib import admin
from .models import Appel
from common.models import UserAppel, EntrepriseAppel, ContactAppel, CandidatureAppel, RelanceAppel

@admin.register(Appel)
class AppelAdmin(admin.ModelAdmin):
    list_display = ("id", "get_user", "subject", "get_candidature", "get_company", "get_contact", "get_relance", "date")
    search_fields = ("subject",)
    list_filter = ("date",)

    def get_user(self, obj):
        relation = UserAppel.objects.filter(appel_id=obj.id).first()
        return relation.user_id if relation else None
    get_user.short_description = 'User'

    def get_company(self, obj):
        relation = EntrepriseAppel.objects.filter(appel_id=obj.id).first()
        return relation.entreprise_id if relation else None
    get_company.short_description = 'Entreprise'

    def get_contact(self, obj):
        relation = ContactAppel.objects.filter(appel_id=obj.id).first()
        return relation.contact_id if relation else None
    get_contact.short_description = 'Contact'

    def get_candidature(self, obj):
        relation = CandidatureAppel.objects.filter(appel_id=obj.id).first()
        return relation.candidature_id if relation else None
    get_candidature.short_description = 'Candidature'

    def get_relance(self, obj):
        relation = RelanceAppel.objects.filter(appel_id=obj.id).first()
        return relation.relance_id if relation else None
    get_relance.short_description = 'Relance'
