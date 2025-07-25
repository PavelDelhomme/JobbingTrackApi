from apps.events.models import Event
from django.db import models
from apps.applications.models import Application
from apps.companies.models import Company
from apps.contacts.models import Contact


class CallService:
    @staticmethod
    def on_create(call):
        Event.objects.create(
            user=call.user,
            title=f"Appel – {call.title}",
            event_type_ref_id="EVENT_TYPE_CALL_SENT",
            start_ts=call.call_ts,
            related_object_type="CALL",
            related_object_id=call.id
        )
        Application.objects.filter(pk=call.application_id)\
            .update(call_ids=models.F("call_ids") + [call.id])
        Company.objects.filter(pk=call.company_id)\
            .update(call_ids=models.F("call_ids") + [call.id])
        Contact.objects.filter(pk=call.contact_id)\
            .update(call_ids=models.F("call_ids") + [call.id])
        

    @staticmethod
    def on_update(call, old_ts):
        if call.call_ts == old_ts:
            return
        Event.objects.filter(
            related_object_id=call.id,
            related_object_type="CALL"
        ).update(start_ts=models.F("start_ts") + (call.call_ts - old_ts))
