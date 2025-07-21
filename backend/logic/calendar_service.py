# backend/logic/calendar_service.py
from apps.events.models import Event
from apps.calendar.models import Calendar
from django.db import transaction

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
        
    @staticmethod
    @transaction.atomic
    def set_as_default(calendar: Calendar):
        # Désactive l’ancien calendrier par défaut de l’utilisateur
        Calendar.objects.filter(
            user=calendar.user, is_default=True
        ).exclude(pk=calendar.pk).update(is_default=False)

        calendar.is_default = True
        calendar.save(update_fields=['is_default'])
