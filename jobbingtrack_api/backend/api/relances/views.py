from rest_framework import viewsets, permissions
from .models import Relance
from .serializers import RelanceSerializer

from api.entreprises.models import Entreprise
from api.evenements.models import Event

class RelanceViewSet(viewsets.ModelViewSet):
    serializer_class = RelanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Relance.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        data = self.request.data
        company_name = data.get("companyName")
        
        entreprise, created = Entreprise.objects.get_or_create(
            name = company_name,
            defaults={
                "user": self.request.user,
                "type": data.get("companyType", ""),
                "phone": data.get("companyPhone", ""),
                "email": data.get("companyEmail", ""),
                "hr_email": data.get("companyHrEmail", ""),
                "address": data.get("companyAddress", ""),
                "notes": data.get("companyNotes", ""),
            }
        )
        
        candidature = serializer.save(user=self.request.user, entreprise=entreprise)
        
        Event.objects.create(
            user=self.request.user,
            title=data.get("title", "Candidature"),
            description=f"Candidature '{candidature.title}' pour {entreprise.name}",
            type="application",
            related_object_id=candidature.id
        )
        
        
        serializer.save(user=self.request.user)


    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
