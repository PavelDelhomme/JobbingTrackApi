from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Entretien
from .serializers import EntretienSerializer
from api.entreprises.models import Entreprise
from api.evenements.models import Event
from common.models.linking_models import UserEntretien

class EntretienViewSet(viewsets.ModelViewSet):
    serializer_class = EntretienSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Entretien.objects.filter(user=self.request.user)


    def perform_create(self, serializer):
        entretien = serializer.save(user_id=self.request.user.id)
        
        UserEntretien.objects.get_or_create(user_id=self.request.user.id, entretien_id=entretien.id)
        
        # Créer événement
        Event.objects.create(
            user_id=self.request.user.id,
            title="Entretien programmé",
            description=f"Entretien prévu le {entretien.date_time}",
            type="interview",
            related_object_id=entretien.id,
        )


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
