# backend/logic/interview_service.py
from apps.events.models import Event

class InterviewService:
    @staticmethod
    def on_create(interview):
        Event.objects.create(
            user               = interview.user,
            title              = f"Entretien – {interview.title or interview.application_id}",
            event_type_ref_id  = 'EVENT_TYPE_INTERVIEW',
            start_ts           = interview.interview_ts,
            related_object_id  = interview.id,
            related_object_type='INTERVIEW',
            notification_enabled=True
        )
