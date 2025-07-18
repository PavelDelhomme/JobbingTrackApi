from apps.events.models import Event
from django.utils import timezone

class ApplicationService:
    @staticmethod
    def create_initial_events(application):
        # Event « Candidature envoyée »
        Event.objects.create(
            user=application.user,
            title=f"Candidature : {application.title}",
            event_type_ref_id='EVENT_TYPE_APPLICATION_SENT',
            start_ts=application.application_ts,
            related_object_id=application.id,
            related_object_type='APPLICATION',
        )
        # Event de relance automatique 7 jours après
        tslater = application.application_ts + 7 * 24 * 3600
        Event.objects.create(
            user=application.user,
            title=f"Relance : {application.title}",
            event_type_ref_id='EVENT_TYPE_FOLLOWUP_REMINDER',
            start_ts=tslater,
            related_object_id=application.id,
            related_object_type='APPLICATION',
            notification_enabled=True,
        )

    @staticmethod
    def update_events(application, old_ts):
        """Si la date change → on décale les événements liés."""
        if application.application_ts == old_ts:
            return
        for ev in Event.objects.filter(
            related_object_id=application.id,
            related_object_type='APPLICATION'
        ):
            delta = application.application_ts - old_ts
            ev.start_ts += delta
            if ev.end_ts:
                ev.end_ts += delta
            ev.save(update_fields=['start_ts', 'end_ts'])
            
    
    def on_create(app):
        Event.objects.create(
            user               = app.user,
            title              = f"Candidature envoyée – {app.title}",
            event_type_ref_id  = 'EVENT_TYPE_APPLICATION_SENT',
            start_ts           = app.application_ts,
            related_object_id  = app.id,
            related_object_type= 'APPLICATION',
        )
        # Relance automatique J+7
        Event.objects.create(
            user              = app.user,
            title             = f"Relance – {app.title}",
            event_type_ref_id = 'EVENT_TYPE_FOLLOWUP_REMINDER',
            start_ts          = app.application_ts + 7*24*3600,
            related_object_id = app.id,
            related_object_type='APPLICATION',
            notification_enabled = True,
        )

    @staticmethod
    def on_update(app, old):
        if app.application_ts != old.application_ts:
            delta = app.application_ts - old.application_ts
            Event.objects.filter(
                related_object_id=app.id,
                related_object_type='APPLICATION'
            ).update(start_ts=models.F('start_ts') + delta)
