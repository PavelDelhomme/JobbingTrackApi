from apps.events.models import Event
from apps.applications.models import Application
from apps.companies.models import Company
from apps.contacts.models import Contact
from apps.interviews.models import Interview
from django.db import models

class InterviewService:
    @staticmethod
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
        # garantie du lien Application -> interview_ids
        Application.objects.filter(pk=itw.application_id).update(
            interview_ids=models.F("interview_ids") + [itw.id]
        )
        Company.objects.filter(pk=itw.company_id).update(
            interview_ids=models.F("interview_ids") + [itw.id]
        )
        # Gestion des contacts multiples
        if itw.contact_ids:  # Liste des IDs de contacts
            for contact_id in itw.contact_ids:
                Contact.objects.filter(pk=contact_id).update(
                    interview_ids=models.F("interview_ids") + [itw.id]
                )
        
    @staticmethod
    def on_update(itw, old):
        if itw.interview_ts == old.interview_ts:
            return
        delta = itw.interview_ts - old.interview_ts
        Event.objects.filter(
            related_object_id=itw.id,
            related_object_type="INTERVIEW"
        ).update(start_ts=models.F("start_ts") + delta)
        # Si le statut devien "Réalisé"
        if itw.status_ref_id == 'ITW_STATUS_DONE' and old.status_ref_id != 'ITW_STATUS_DONE':
            # Compter le nomre nombre d'entretiens pour cette candidature
            count = Interview.objects.filter(
                application_id=itw.application_id,
                status_ref_id='ITW_STATUS_DONE'
            ).count()
            
            if count == 1:
                new_status = 'APP_STATUS_ITW_1'
            else:
                new_status = 'APP_STATUS_ITW_N'
            
            Application.objects.filter(pk=itw.application_id).update(
                status_ref_id=new_status
            )