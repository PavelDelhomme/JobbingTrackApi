from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrAdmin


class BaseViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user, is_deleted=False)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
