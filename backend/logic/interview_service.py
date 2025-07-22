from apps.events.models import Event
from apps.applications.models import Application
from apps.companies.models import Company
from apps.contacts.models import Contact
from apps.interviews.models import Interview
from django.db import models
from django.db import transaction

class InterviewService:
    @staticmethod
    @transaction.atomic
    def create_or_update_interview(data, user):
        """
        Crée ou met à jour un entretien avec gestion des entités liées
        """
        # Vérifier si la candidature existe
        application_id = data.get('application_id')
        if not application_id:
            raise ValueError("Un entretien doit être lié à une candidature")
        
        # Vérifier si l'entreprise existe, sinon récupérer celle de la candidature
        company_id = data.get('company_id')
        if not company_id:
            # Récupérer l'entreprise à partir de la candidature
            from apps.applications.models import Application
            try:
                application = Application.objects.get(id=application_id, user=user)
                data['company_id'] = str(application.company_id)
                # Ajouter également company_name pour cohérence
                data['company_name'] = application.company_name
            except Application.DoesNotExist:
                raise ValueError("La candidature associée n'existe pas")
        
        # Gérer les contacts associés
        contact_ids = data.get('contact_ids', [])
        contact_names = data.get('contact_names', [])
        
        # Si des noms de contacts sont fournis mais pas d'IDs, créer des contacts
        if contact_names and not contact_ids:
            contact_ids = []
            from apps.contacts.services import ContactService
            for i, name in enumerate(contact_names):
                position = data.get('contact_positions', [])[i] if i < len(data.get('contact_positions', [])) else ''
                contact = ContactService.create_minimal_contact(
                    name=name,
                    position=position,
                    company_id=data.get('company_id'),
                    user=user
                )
                contact_ids.append(str(contact.id))
            
            # Mettre à jour les IDs de contact dans les données
            data['contact_ids'] = contact_ids
        
        # Créer ou mettre à jour l'entretien
        from apps.common.sync import SyncService
        interview, created = SyncService.update_from_client(
            'interviews.Interview',
            data,
            user
        )
        
        # Créer un événement pour cet entretien
        if created:
            from apps.events.services import EventService
            EventService.create_interview_event(interview)
            
        return interview, created
    
    @staticmethod
    @transaction.atomic
    def create_or_update_from_client(data, user):
        pass
    
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