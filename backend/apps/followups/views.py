from apps.common.viewsets import BaseViewSet
from .models import FollowUp
from .serializers import FollowUpSerializer

class FollowUpViewSet(BaseViewSet):
    queryset = FollowUp.objects.all()
    serializer_class = FollowUpSerializer