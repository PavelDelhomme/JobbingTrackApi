from apps.common.utils.factory import crud_viewset
from .models import Calendar
from .serializers import CalendarSerializer
from logic.calendar_service import CalendarService
"""
class _CalendarVS(crud_viewset(Calendar, CalendarSerializer)):
    def perform_create(self, serializer):
        cal = serializer.save(user=self.request.user)
        CalendarService.set_as_default(cal)

CalendarViewSet = _CalendarVS
"""

CalendarViewSet = crud_viewset(
    Calendar,
    CalendarSerializer,
    on_create=CalendarService.set_as_default
)