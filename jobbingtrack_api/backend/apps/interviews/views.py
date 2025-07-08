#backend/api/entretiens/views.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Interview
from .serializers import InterviewSerializer
from apps.companies.models import Company
from apps.calendar.models import Event
from api.common.models import UserInterview

class InterviewViewSet(viewsets.ModelViewSet):
    serializer_class = InterviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Interview.objects.filter(user=self.request.user)


    def perform_create(self, serializer):
        interview = serializer.save(user_id=self.request.user.id)
        
        UserInterview.objects.get_or_create(user_id=self.request.user.id, interview_id=interview.id)
        
        # Créer événement
        Event.objects.create(
            user_id=self.request.user.id,
            title="Entretien programmé",
            description=f"Entretien prévu le {interview.date_time}",
            type="interview",
            related_object_id=interview.id,
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
