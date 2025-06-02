from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Contact
from .serializers import ContactSerializer
from api.entreprises.models import Entreprise
from common.models.linking_models import UserContact, ContactEntreprise

from django.utils import timezone

class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        data = self.request.data
        user = self.request.user
        
        
        company_name = data.get("companyName")
        entreprise = None
        
        if company_name:                    
            entreprise, _ = Entreprise.objects.get_or_create(
                name = company_name,
                defaults={
                    "user": user,
                    "type": data.get("companyType", ""),
                    "phone": data.get("companyPhone", ""),
                    "email": data.get("companyEmail", ""),
                    "hr_email": data.get("companyHrEmail", ""),
                    "address": data.get("companyAddress", ""),
                    "notes": data.get("companyNotes", ""),
                    "sync_hash": data.get("companySyncHash", ""),
                }
            )
        
        contact = serializer.save(user=user)
        
        UserContact.objects.get_or_create(user_id=str(user.id), contact_id=str(contact.id))
        
        if entreprise:
            ContactEntreprise.objects.get_or_create(contact_id=str(contact.id), entreprise_id=str(entreprise.id))
        
        # serializer.save(user=user)

    # --- Récupérer archivés ---
    @action(detail=False, methods=["get"], url_path="archived")
    def archived(self, request):
        queryset = self.get_queryset().filter(is_archived=True)
        return Response(self.get_serializer(queryset, many=True).data)

    # --- Récupérer actifs ---
    @action(detail=False, methods=["get"], url_path="active")
    def active(self, request):
        queryset = self.get_queryset().filter(is_archived=False, is_deleted=False)
        return Response(self.get_serializer(queryset, many=True).data)

    # --- Récupérer supprimés ---
    @action(detail=False, methods=["get"], url_path="deleted")
    def deleted(self, request):
        queryset = self.get_queryset().filter(is_deleted=True)
        return Response(self.get_serializer(queryset, many=True).data)

    # --- Soft delete (mettre is_deleted à True + timestamp) ---
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.save()