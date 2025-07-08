from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.timezone import now
from django.db.models import Q

from .models import FollowUp
from .serializers import FollowUpSerializer
from apps.companies.models import Company
from apps.calendar.models import Event

class FollowUpViewSet(viewsets.ModelViewSet):
    serializer_class = FollowUpSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FollowUp.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def perform_update(self, serializer):
        serializer.save(user_id=self.request.user.id)

    @action(detail=False, methods=["get"], url_path="archived")
    def archived(self, request):
        return self._list_filtered(is_archived=True, is_deleted=False)

    @action(detail=False, methods=["get"], url_path="active")
    def active(self, request):
        return self._list_filtered(is_archived=False, is_deleted=False)

    @action(detail=False, methods=["get"], url_path="deleted")
    def deleted(self, request):
        return self._list_filtered(is_deleted=True)

    @action(detail=False, methods=["get"], url_path="date-range")
    def date_range(self, request):
        from_date = request.query_params.get("from")
        to_date = request.query_params.get("to")

        if not from_date or not to_date:
            return Response({"error": "Missing 'from' or 'to' parameter"}, status=400)

        qs = self.get_queryset().filter(date__gte=from_date, date__lte=to_date)
        return Response(self.get_serializer(qs, many=True).data)

    @action(detail=False, methods=["post"], url_path="archive")
    def archive(self, request):
        ids = request.data.get("ids", [])
        qs = self.get_queryset().filter(id__in=ids)
        qs.update(is_archived=True, archived_at=now())
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["post"], url_path="soft-delete")
    def soft_delete(self, request):
        ids = request.data.get("ids", [])
        qs = self.get_queryset().filter(id__in=ids)
        qs.update(is_deleted=True, deleted_at=now())
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["post"], url_path="restore")
    def restore(self, request):
        ids = request.data.get("ids", [])
        qs = self.get_queryset().filter(id__in=ids)
        qs.update(is_deleted=False)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["post"], url_path="delete-forever")
    def delete_forever(self, request):
        ids = request.data.get("ids", [])
        self.get_queryset().filter(id__in=ids).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _list_filtered(self, **filters):
        qs = self.get_queryset().filter(**filters)
        return Response(self.get_serializer(qs, many=True).data)
