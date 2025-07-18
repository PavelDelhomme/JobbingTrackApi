from django.utils import timezone
from apps.events.models import Event

class EventService:
    @staticmethod
    def pending_notifications():
        now = int(timezone.now().timestamp())
        return Event.objects.filter(
            notification_enabled=True,
            start_ts__lte=now + 900
        )
