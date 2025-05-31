from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import datetime
from .models import Appel
from .serializers import AppelSerializer

class AppelViewSet(viewsets.ModelViewSet):
    serializer_class = AppelSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Appel.objects.filter(user=self.request.user)

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

        appels = Appel.objects.filter(user=user, date_time__range=(from_dt, to_dt))
        return Response(self.get_serializer(appels, many=True).data)

class AppelList(APIView):
    def get(self, request):
        return Response({"message": "Liste des appels"})

class AppelDetail(APIView):
    def get(self, request, pk):
        return Response({"message": f"Détails de l'appel {pk}"})
    
