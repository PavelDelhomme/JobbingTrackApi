# apps/interviews/services.py
from django.db import transaction
import uuid
import time

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
                if application.company_id:
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