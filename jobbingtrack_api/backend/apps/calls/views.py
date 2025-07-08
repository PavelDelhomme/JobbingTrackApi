from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import datetime
from .models import Call
from .serializers import CallSerializer
from django.shortcuts import get_object_or_404

class CallViewSet(viewsets.ModelViewSet):
    serializer_class = CallSerializer
    permission_classes = [permissions.IsAuthenticated]
        
    def get_queryset(self):
        queryset = Call.objects.filter(user=self.request.user.id)

        application_id = self.request.query_params.get("application_id")
        company_id = self.request.query_params.get("company_id")
        followup_id = self.request.query_params.get("followup_id")

        if application_id:
            queryset = queryset.filter(application_id=application_id)
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        if followup_id:
            queryset = queryset.filter(followup_id=followup_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"], url_path="archived")
    def archived(self, request):
        calls = self.get_queryset().filter(is_archived=True)
        return Response(self.get_serializer(calls, many=True).data)

    @action(detail=False, methods=["get"], url_path="active")
    def active(self, request):
        calls = self.get_queryset().filter(is_archived=False, is_deleted=False)
        return Response(self.get_serializer(calls, many=True).data)

    @action(detail=False, methods=["get"], url_path="deleted")
    def deleted(self, request):
        calls = self.get_queryset().filter(is_deleted=True)
        return Response(self.get_serializer(calls, many=True).data)

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

        calls = Call.objects.filter(user_id=user.id, date__range=(from_dt, to_dt))
        return Response(self.get_serializer(calls, many=True).data)

class CallList(APIView):
    def get(self, request):
        return Response({"message": "Liste des appels"})

class CallDetail(APIView):
    def get(self, request, pk):
        return Response({"message": f"Détails de l'appel {pk}"})
    
