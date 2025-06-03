from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Entreprise
from .serializers import EntrepriseSerializer
from common.models import UserEntreprise
from django.utils import timezone


class EntrepriseViewSet(viewsets.ModelViewSet):
    serializer_class = EntrepriseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Entreprise.objects.filter(user_id=self.request.user.id, is_deleted=False)

    def perform_create(self, serializer):
        data = self.request.data
        name = data.get("name", "").strip()

        if not name:
            raise ValueError("Le nom de l'entreprise est requis")

        entreprise = Entreprise.objects.filter(name=name).first()

        if entreprise:
            # Mise à jour partielle si elle existe déjà
            entreprise.type = data.get("type", entreprise.type)
            entreprise.phone = data.get("phone", entreprise.phone)
            entreprise.email = data.get("email", entreprise.email)
            entreprise.hr_email = data.get("hr_email", entreprise.hr_email)
            entreprise.address = data.get("address", entreprise.address)
            entreprise.notes = data.get("notes", entreprise.notes)
            entreprise.updated_at = timezone.now()
            entreprise.save()
        else:
            # Création
            entreprise = serializer.save(user_id=self.request.user.id)

        # Création de la relation UserEntreprise si absente
        UserEntreprise.objects.get_or_create(
            user_id=self.request.user.id,
            entreprise_id=entreprise.id
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
