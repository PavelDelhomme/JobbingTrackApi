from apps.events.models import Event
from django.db import models

class InterviewService:
    def on_create(itw):
        Event.objects.create(
            user=itw.user,
            title=f"Entretien – {itw.title or 'Sans titre'}",
            event_type_ref_id="EVENT_TYPE_INTERVIEW_SCHEDULED",
            start_ts=itw.interview_ts,
            related_object_type="INTERVIEW",
            related_object_id=itw.id,
            notification_enabled=True
        )

    def on_update(itw, old):
        if itw.interview_ts == old.interview_ts:
            return
        delta = itw.interview_ts - old.interview_ts
        Event.objects.filter(
            related_object_id=itw.id,
            related_object_type="INTERVIEW"
        ).update(start_ts=models.F("start_ts") + delta)
