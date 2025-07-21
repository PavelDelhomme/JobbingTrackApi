# backend/logic/followup_service.py
from apps.events.models import Event
from apps.applications.models import Application
from apps.companies.models import Company
from apps.contacts.models import Contact
from django.db import models
from apps.references.models import Reference

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
        # Ajoute l'ID de follow-up à Application et Company
        Application.objects.filter(pk=fu.application_id)\
            .update(followup_ids=models.F('followup_ids') + [fu.id])
        Company.objects.filter(pk=fu.company_id)\
            .update(followup_ids=models.F('followup_ids') + [fu.id])
        Contact.objects.filter(pk=fu.contact_id)\
            .update(followup_ids=models.F('followup_ids') + [fu.id])
        
        
        # mise à jour du statut de la relance
        fu.status_ref_id = 'FU_STATUS_PENDING'
        fu.save(update_fields=['status_ref_id'])

        # impact candidature
        Application.objects.filter(pk=fu.application_id).update(
            status_ref_id='APP_STATUS_NO_REPLY'
        )
    
    def on_update(fu, old_status):
        if fu.status_ref_id == 'FU_STATUS_NEGATIVE' and old_status != 'FU_STATUS_NEGATIVE':
            Application.objects.filter(pk=fu.application_id).update(
                status_ref_id='APP_STATUS_REJECTED_NO_ITW'
            )
        elif fu.status_ref_id == 'FU_STATUS_POSITIVE' and old_status != 'FU_STATUS_POSITIVE':
            Application.objects.filter(pk=fu.application_id).update(
                status_ref_id='APP_STATUS_INTERVIEW'
            )
        elif fu.status_ref_id == 'FU_STATUS_NO_REPLY' and old_status != 'FU_STATUS_NO_REPLY':
            Application.objects.filter(pk=fu.application_id).update(
                status_ref_id='APP_STATUS_NO_REPLY'
            )
        