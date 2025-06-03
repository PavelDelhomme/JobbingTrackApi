from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Candidature
from api.entreprises.models import Entreprise
from api.evenements.models import Event
from .serializers import CandidatureSerializer

class CandidatureViewSet(viewsets.ModelViewSet):
    serializer_class = CandidatureSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Candidature.objects.filter(user=self.request.user)
def perform_create(self, serializer):
    data = self.request.data
    company_name = data.get("companyName")
    
    entreprise, _ = Entreprise.objects.get_or_create(
        name = company_name,
        defaults={
            "user_id": self.request.user.id,
            "type": data.get("companyType", ""),
            "phone": data.get("companyPhone", ""),
            "email": data.get("companyEmail", ""),
            "hr_email": data.get("companyHrEmail", ""),
            "address": data.get("companyAddress", ""),
            "notes": data.get("companyNotes", ""),
        }
    )
    
    serializer.save(
        user_id=self.request.user.id,
        entreprise_id=entreprise.id
    )

    Event.objects.create(
        user_id=self.request.user.id,
        title=data.get("title", "Candidature"),
        description=f"Candidature '{serializer.validated_data.get('title')}' pour {entreprise.name}",
        type="application",
        related_object_id=serializer.instance.id
    )

    @action(detail=False, methods=["get"], url_path="archived")
    def archived(self, request):
        return Response(self.get_serializer(
            self.get_queryset().filter(is_archived=True), many=True).data)

    @action(detail=False, methods=["get"], url_path="active")
    def active(self, request):
        return Response(self.get_serializer(
            self.get_queryset().filter(is_archived=False, is_deleted=False), many=True).data)

    @action(detail=False, methods=["get"], url_path="deleted")
    def deleted(self, request):
        return Response(self.get_serializer(
            self.get_queryset().filter(is_deleted=True), many=True).data)

    @action(detail=False, methods=["get"], url_path="by-date-range")
    def date_range(self, request):
        user = request.user
        from_ts = request.query_params.get("from")
        to_ts = request.query_params.get("to")

        try:
            from_dt = datetime.fromtimestamp(int(from_ts) / 1000)
            to_dt = datetime.fromtimestamp(int(to_ts) / 1000)
        except:
            return Response({"error": "Invalid timestamps"}, status=400)

        appels = Appel.objects.filter(user=user, date_time__range=(from_dt, to_dt))
        return Response(self.get_serializer(appels, many=True).data)
    