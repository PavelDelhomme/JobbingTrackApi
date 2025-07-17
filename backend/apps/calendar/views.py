from apps.common.viewsets import BaseViewSet
from .models import Calendar
from .serializers import CalendarSerializer

class CalendarViewSet(BaseViewSet):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer
