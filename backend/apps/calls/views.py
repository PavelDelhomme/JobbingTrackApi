#from apps.common.viewsets import BaseViewSet
from apps.common.utils.factory import crud_viewset
from .models import Call
from .serializers import CallSerializer
from logic.call_service import CallService

"""
class CallViewSet(BaseViewSet):
    queryset = Call.objects.all()
    serializer_class = CallSerializer

    def perform_create(self, serializer):
        call = serializer.save(user=self.request.user)
        CallService.on_create(call)

    def perform_update(self, serializer):
        old = self.get_object()
        call = serializer.save()
        CallService.on_update(call, old.call_ts)
"""

CallViewSet = crud_viewset(
    Call,
    CallSerializer,
    on_create=CallService.on_create,
    on_update=lambda c: CallService.on_update(c, c.call_ts)
)