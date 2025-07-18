# backend/logic/followup_service.py
from apps.events.models import Event

class FollowUpService:
    @staticmethod
    def on_create(fu):
        Event.objects.create(
            user = fu.user,
            title = f"Relance effectuée – {fu.title or 'sans titre'}",
            event_type_ref_id='EVENT_TYPE_FOLLOWUP_DONE',
            start_ts = fu.followup_ts,
            related_object_id = fu.id,
            related_object_type='FOLLOWUP',
        )
        if fu.next_followup_ts:
            Event.objects.create(
                user = fu.user,
                title = f"Relance suivante – {fu.title or 'sans titre'}",
                event_type_ref_id='EVENT_TYPE_FOLLOWUP_REMINDER',
                start_ts = fu.next_followup_ts,
                related_object_id = fu.id,
                related_object_type='FOLLOWUP',
                notification_enabled = True,
            )
