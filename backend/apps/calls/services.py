# apps/calls/services.py
from django.db import transaction
import uuid
import time

class CallService:
    @staticmethod
    @transaction.atomic
    def create_or_update_call(data, user):
        """
        Crée ou met à jour un appel avec gestion des entités liées
        """
        # Vérifier/créer la company si nécessaire
        company_id = data.get('company_id')
        company_name = data.get('company_name')
        
        if not company_id and company_name:
            from apps.companies.services import CompanyService
            company = CompanyService.create_minimal_company(company_name, user)
            data['company_id'] = str(company.id)
        
        # Vérifier/créer le contact si nécessaire
        contact_id = data.get('contact_id')
        contact_name = data.get('contact_name')
        contact_position = data.get('contact_position', '')
        
        if not contact_id and contact_name:
            from apps.contacts.services import ContactService
            contact = ContactService.create_minimal_contact(
                name=contact_name, 
                position=contact_position,
                company_id=data.get('company_id'),
                user=user
            )
            data['contact_id'] = str(contact.id)
        
        # Créer ou mettre à jour l'appel
        from apps.common.sync import SyncService
        call, created = SyncService.update_from_client(
            'calls.Call', 
            data, 
            user
        )
        
        # Créer une candidature si c'est un appel entrant sans candidature liée
        application_id = data.get('application_id')
        if not application_id and data.get('is_inbound', False) and data.get('create_application', False):
            from apps.applications.services import ApplicationService
            app_data = {
                'title': data.get('application_title', f"Candidature suite à l'appel du {time.strftime('%d/%m/%Y')}"),
                'company_id': data.get('company_id'),
                'company_name': data.get('company_name'),
                'application_ts': call.call_ts,  # Même date que l'appel
                'notes': f"Créé automatiquement suite à l'appel {call.id}"
            }
            application, _ = ApplicationService.create_or_update_application(app_data, user)
            
            # Lier l'appel à la candidature
            call.application_id = application.id
            call.save()
        
        # Créer un événement pour cet appel
        if created:
            from apps.events.services import EventService
            EventService.create_call_event(call)
            
        return call, created
    
    @staticmethod
    def get_call_stats(user, period_days=30):
        """
        Récupère les statistiques d'appels
        """
        from apps.calls.models import Call
        from datetime import datetime, timedelta
        
        # Calcul des dates
        end_date = datetime.now()
        start_date = end_date - timedelta(days=period_days)
        
        # Conversion en timestamps
        start_ts = int(start_date.timestamp() * 1000)
        end_ts = int(end_date.timestamp() * 1000)
        
        # Récupération des appels
        calls = Call.objects.filter(
            user=user,
            call_ts__gte=start_ts,
            call_ts__lte=end_ts,
            is_deleted=False
        )
        
        # Statistiques
        total_calls = calls.count()
        incoming_calls = calls.filter(is_inbound=True).count()
        outgoing_calls = total_calls - incoming_calls
        
        # Durée moyenne
        durations = [call.duration_minutes for call in calls if call.duration_minutes]
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        return {
            'total': total_calls,
            'incoming': incoming_calls,
            'outgoing': outgoing_calls,
            'avg_duration': avg_duration
        }