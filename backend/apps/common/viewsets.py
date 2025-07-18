from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly

class BaseViewSet(viewsets.ModelViewSet):
    """
    ViewSet générique :
    • filtre par user
    • soft-delete / archive
    • synchronisation via ?updated_after=
    """
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    

    # --- Queryset -------------------------------------------------
    def get_queryset(self):
        qs = self.queryset.filter(user=self.request.user, is_deleted=False)
        since = self.request.query_params.get("updated_after")
        if since:
            qs = qs.filter(updated_at__gt=since)
        return qs.order_by("-updated_at")

    # --- Création -------------------------------------------------
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # --- Actions custom ------------------------------------------
    @action(detail=True, methods=["post"])
    def soft_delete(self, request, pk=None):
        obj = self.get_object()
        obj.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def archive(self, request, pk=None):
        obj = self.get_object()
        obj.archive()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def restore(self, request, pk=None):
        obj = self.get_object()
        obj.restore()
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def archived(self, request):
        data = self.get_serializer(
            self.queryset.filter(
                user=request.user, is_archived=True, is_deleted=False
            ),
            many=True,
        ).data
        return Response(data)

    @action(detail=False, methods=["get"])
    def deleted(self, request):
        data = self.get_serializer(
            self.queryset.filter(user=request.user, is_deleted=True), many=True
        ).data
        return Response(data)