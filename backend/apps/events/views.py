from apps.common.utils.factory import crud_viewset
from .models import Event
from .serializers import EventSerializer
from logic.event_service import EventService

class _EventVS(crud_viewset(Event, EventSerializer)):
    def perform_create(self, serializer):
        event = serializer.save(user=self.request.user)
        EventService.on_create(event)

    def perform_update(self, serializer):
        event = serializer.save()
        EventService.on_update(event)

EventViewSet = _EventVS
