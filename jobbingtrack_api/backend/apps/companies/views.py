from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Company
from .serializers import CompanySerializer
from api.common.models import UserCompany
from django.utils import timezone


class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Company.objects.filter(user_id=self.request.user.id, is_deleted=False)

    def perform_create(self, serializer):
        data = self.request.data
        name = data.get("name", "").strip()

        if not name:
            raise ValueError("Le nom de l'entreprise est requis")

        company = Company.objects.filter(name=name).first()

        if company:
            # Mise à jour partielle si elle existe déjà
            company.type = data.get("type", company.type)
            company.phone = data.get("phone", company.phone)
            company.email = data.get("email", company.email)
            company.hr_email = data.get("hr_email", company.hr_email)
            company.address = data.get("address", company.address)
            company.notes = data.get("notes", company.notes)
            company.updated_at = timezone.now()
            company.save()
        else:
            # Création
            company = serializer.save(user_id=self.request.user.id)

        # Création de la relation UserEntreprise si absente
        UserCompany.objects.get_or_create(
            user_id=self.request.user.id,
            company_id=company.id
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
