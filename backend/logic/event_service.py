# backend/logic/event_service.py
from django.utils import timezone
from django.core.mail import send_mail

class EventService:
    @staticmethod
    def check_notifications():
        now_ts = int(timezone.now().timestamp())
        from apps.events.models import Event
        qs = Event.objects.filter(
            notification_enabled=True,
            start_ts__lte=now_ts + 900,     # 15 min avant
            is_deleted=False,
            is_archived=False
        )
        for ev in qs:
            send_mail(
                subject=ev.title,
                message=ev.description or ev.title,
                from_email='noreply@jobbingtrack',
                recipient_list=[ev.user.email],
                fail_silently=True
            )
            ev.notification_enabled = False
            ev.save(update_fields=['notification_enabled'])
