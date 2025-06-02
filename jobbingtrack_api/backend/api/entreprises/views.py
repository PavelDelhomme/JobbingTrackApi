from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Entreprise
from .serializers import EntrepriseSerializer

class EntrepriseViewSet(viewsets.ModelViewSet):
    serializer_class = EntrepriseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Entreprise.objects.filter(user=self.request.user)

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
        
        entreprise = serializer.save(user=self.request.user, entreprise=entreprise)
                
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
