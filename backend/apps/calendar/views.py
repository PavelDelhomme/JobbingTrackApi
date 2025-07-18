from apps.common.utils.factory import crud_viewset
from .models import Calendar
from .serializers import CalendarSerializer

CalendarViewSet = crud_viewset(Calendar, CalendarSerializer)