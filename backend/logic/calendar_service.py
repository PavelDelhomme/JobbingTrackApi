# backend/logic/calendar_service.py
from apps.events.models import Event
from apps.calendar.models import Calendar

class CalendarService:
    @staticmethod
    def default_calendar(user):
        cal, _ = Calendar.objects.get_or_create(
            user=user, is_default=True,
            defaults={"name": "Calendrier principal"}
        )
        return cal

    @staticmethod
    def events_between(user, start_ts, end_ts):
        return Event.objects.filter(
            user=user,
            start_ts__gte=start_ts,
            start_ts__lte=end_ts,
            is_deleted=False
        )
