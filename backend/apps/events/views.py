from apps.common.viewsets import BaseViewSet
from .models import Event
from .serializers import EventSerializer
from backend.apps.common.utils.factory import viewset_factory
from logic.event_service import EventService

#class EventViewSet(BaseViewSet):
#    queryset = Event.objects.all()
#    serializer_class = EventSerializer

EventViewSet = viewset_factory(Event, EventSerializer)