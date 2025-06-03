from django.contrib import admin
from .models import Relance
from common.models import ContactRelance, CandidatureRelance, EntrepriseRelance

@admin.register(Relance)
class RelanceAdmin(admin.ModelAdmin):
    list_display = ("id", "get_candidature", "get_entreprise", "date", "status")

    def get_candidature(self, obj):
        rel = CandidatureRelance.objects.filter(relance_id=obj.id).first()
        return rel.candidature_id if rel else None
    get_candidature.short_description = "Candidature"

    def get_entreprise(self, obj):
        rel = EntrepriseRelance.objects.filter(relance_id=obj.id).first()
        return rel.entreprise_id if rel else None
    get_entreprise.short_description = "Entreprise"

@admin.register(ContactRelance)
class RelanceContactAdmin(admin.ModelAdmin):
    list_display = ("relance_id", "contact_id")
