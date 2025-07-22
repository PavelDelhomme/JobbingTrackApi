# apps/followups/services.py
from django.db import transaction
import uuid
import time

class FollowUpService:
    @staticmethod
    @transaction.atomic
    def create_or_update_followup(data, user):
        """
        Crée ou met à jour une relance avec gestion des entités liées
        """
        # Une relance doit toujours être liée à une candidature
        application_id = data.get('application_id')
        if not application_id:
            raise ValueError("Une relance doit être liée à une candidature")
        
        # Récupérer l'entreprise de la candidature si non spécifiée
        company_id = data.get('company_id')
        if not company_id:
            from apps.applications.models import Application
            try:
                application = Application.objects.get(id=application_id, user=user)
                if application.company_id:
                    data['company_id'] = str(application.company_id)
                    # Ajouter company_name pour cohérence
                    data['company_name'] = application.company_name
            except Application.DoesNotExist:
                raise ValueError("La candidature associée n'existe pas")
        
        # Créer ou mettre à jour la relance
        from apps.common.sync import SyncService
        followup, created = SyncService.update_from_client(
            'followups.FollowUp',
            data,
            user
        )
        
        # Créer un événement pour cette relance
        if created:
            from apps.events.services import EventService
            EventService.create_followup_event(followup)
        
        # Mettre à jour le statut de la candidature si nécessaire
        if data.get('update_application_status', False) and data.get('new_application_status_id'):
            from apps.applications.models import Application
            try:
                application = Application.objects.get(id=application_id, user=user)
                application.status_id = data.get('new_application_status_id')
                application.save()
            except Application.DoesNotExist:
                pass
        
        return followup, created
    
    @staticmethod
    def get_pending_followups(user):
        """
        Récupère les relances en attente
        """
        from apps.followups.models import FollowUp
        from datetime import datetime
        
        # Récupérer les relances dont la date est passée mais qui n'ont pas été complétées
        now_ts = int(datetime.now().timestamp() * 1000)
        
        followups = FollowUp.objects.filter(
            user=user,
            followup_ts__lte=now_ts,
            is_completed=False,
            is_deleted=False
        ).order_by('followup_ts')
        
        return followups
    
    @staticmethod
    def mark_as_completed(followup_id, user, result_notes=""):
        """
        Marque une relance comme complétée
        """
        from apps.followups.models import FollowUp
        
        try:
            followup = FollowUp.objects.get(id=followup_id, user=user)
            followup.is_completed = True
            followup.result_notes = result_notes
            followup.completed_ts = int(time.time() * 1000)
            followup.save()
            return followup
        except FollowUp.DoesNotExist:
            return None