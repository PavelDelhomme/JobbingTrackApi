from django.utils import timezone
from django.core.mail import send_mail
from apps.events.models import Event

class EventService:
    @staticmethod
    def pending_notifications():
        now = int(timezone.now().timestamp())
        return Event.objects.filter(
            notification_enabled=True,
            start_ts__lte=now + 900,  # 15 minutes avant
            is_deleted=False
        )
    
    @staticmethod
    def send_notifications():
        """À appeler via un cron job"""
        for event in EventService.pending_notifications():
            # Email notification
            if event.user.userprofile.settings.notif_email:
                send_mail(
                    subject=f"Rappel : {event.title}",
                    message=event.description or f"Événement prévu : {event.title}",
                    from_email='noreply@jobbingtrack.com',
                    recipient_list=[event.user.email],
                    fail_silently=True
                )
            
            # Marque comme envoyé
            event.notification_enabled = False
            event.save(update_fields=['notification_enabled'])
