from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Entretien
from .serializers import EntretienSerializer
from api.entreprises.models import Entreprise

class EntretienViewSet(viewsets.ModelViewSet):
    serializer_class = EntretienSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Entretien.objects.filter(user=self.request.user)


    def perform_create(self, serializer):
        data = self.request.data
        company_name = data.get("companyName")
                
        candidature = serializer.save(user=self.request.user, entreprise=entreprise)
        
        Event.objects.create(
            user=self.request.user,
            title=data.get("title", "Candidature"),
            description=f"Candidature '{candidature.title}' pour {entreprise.name}",
            type="application",
            related_object_id=candidature.id
        )
        
        
        serializer.save(user=self.request.user)


    @action(detail=False, methods=["get"], url_path="archived")
    def archived(self, request):
        queryset = self.get_queryset().filter(is_archived=True)
        return Response(self.get_serializer(queryset, many=True).data)

    @action(detail=False, methods=["get"], url_path="active")
    def active(self, request):
        queryset = self.get_queryset().filter(is_archived=False, is_deleted=False)
        return Response(self.get_serializer(queryset, many=True).data)

    @action(detail=False, methods=["get"], url_path="deleted")
    def deleted(self, request):
        queryset = self.get_queryset().filter(is_deleted=True)
        return Response(self.get_serializer(queryset, many=True).data)
