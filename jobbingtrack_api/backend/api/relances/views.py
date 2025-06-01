from rest_framework import viewsets, permissions
from .models import Relance
from .serializers import RelanceSerializer

class RelanceViewSet(viewsets.ModelViewSet):
    serializer_class = RelanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Relance.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
