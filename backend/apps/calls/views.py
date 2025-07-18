from apps.common.viewsets import BaseViewSet
from .models import Call
from .serializers import CallSerializer
from logic.call_service import CallService


class CallViewSet(BaseViewSet):
    queryset = Call.objects.all()
    serializer_class = CallSerializer
