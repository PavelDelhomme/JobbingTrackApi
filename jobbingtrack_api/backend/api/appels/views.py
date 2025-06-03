from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import datetime
from .models import Appel
from .serializers import AppelSerializer
from django.shortcuts import get_object_or_404

class AppelViewSet(viewsets.ModelViewSet):
    serializer_class = AppelSerializer
    permissions_classes = [permissions.IsAuthenticated]
        
    def get_queryset(self):
        queryset = Appel.objects.filter(user=self.request.user.id)

        candidature_id = self.request.query_params.get("candidature_id")
        entreprise_id = self.request.query_params.get("entreprise_id")
        relance_id = self.request.query_params.get("relance_id")

        if candidature_id:
            queryset = queryset.filter(candidature_id=candidature_id)
        if entreprise_id:
            queryset = queryset.filter(entreprise_id=entreprise_id)
        if relance_id:
            queryset = queryset.filter(relance_id=relance_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"], url_path="archived")
    def archived(self, request):
        appels = self.get_queryset().filter(is_archived=True)
        return Response(self.get_serializer(appels, many=True).data)

    @action(detail=False, methods=["get"], url_path="active")
    def active(self, request):
        appels = self.get_queryset().filter(is_archived=False, is_deleted=False)
        return Response(self.get_serializer(appels, many=True).data)

    @action(detail=False, methods=["get"], url_path="deleted")
    def deleted(self, request):
        appels = self.get_queryset().filter(is_deleted=True)
        return Response(self.get_serializer(appels, many=True).data)

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

        appels = Appel.objects.filter(user_id=user.id, date__range=(from_dt, to_dt))
        return Response(self.get_serializer(appels, many=True).data)

class AppelList(APIView):
    def get(self, request):
        return Response({"message": "Liste des appels"})

class AppelDetail(APIView):
    def get(self, request, pk):
        return Response({"message": f"Détails de l'appel {pk}"})
    
