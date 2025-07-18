from apps.common.viewsets import BaseViewSet
from .models import Calendar
from .serializers import CalendarSerializer
from logic.calendar_service import CalendarService

class CalendarViewSet(BaseViewSet):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer
