from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from .models import Contact
from .serializers import ContactSerializer
from apps.companies.models import Company
from api.common.models import UserContact, ContactCompany


class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        data = self.request.data
        user = self.request.user

        company_name = data.get("companyName")
        company = None

        if company_name:
            company, _ = Company.objects.get_or_create(
                name=company_name,
                defaults={
                    "user_id": user.id,
                    "type": data.get("companyType", ""),
                    "phone": data.get("companyPhone", ""),
                    "email": data.get("companyEmail", ""),
                    "hr_email": data.get("companyHrEmail", ""),
                    "address": data.get("companyAddress", ""),
                    "notes": data.get("companyNotes", ""),
                    "sync_hash": data.get("companySyncHash", ""),
                }
            )

        contact = serializer.save(
            user_id=user.id,
            company_id=company.id if company else None
        )

        UserContact.objects.get_or_create(user_id=str(user.id), contact_id=str(contact.id))

        if company:
            ContactCompany.objects.get_or_create(contact_id=str(contact.id), company_id=str(company.id))

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

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.save()