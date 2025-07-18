from apps.common.viewsets import BaseViewSet
from .models import FollowUp
from .serializers import FollowUpSerializer

from logic.followup_service import FollowUpService

class FollowUpViewSet(BaseViewSet):
    queryset = FollowUp.objects.all()
    serializer_class = FollowUpSerializer

    def perform_create(self, serializer):
        fu = serializer.save(user=self.request.user)
        FollowUpService.on_create(fu)

    def perform_update(self, serializer):
        fu = serializer.save()
        # Si besoin : FollowUpService.on_update(fu, old)
        FollowUpService.on_update(fu)