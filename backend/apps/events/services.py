import uuid
import time

class EventService:
    @staticmethod
    def create_application_event(application):
        """
        Crée un évenement pour une nouvelle candidature
        """
        from apps.events.models import Event
        
        timestamp = int(time.time() * 1000)
        event = Event.objects.create(
            id=str(uuid.uuid4()),
            user=application.user,
            title=f"Candidature - {application.title}",
            description=f"Candidature créée pour {application.company_name}",
            event_ts=application.application_ts,
            duration_minutes=30, # Durée par défaut
            application_id=application.id,
            company_id=application.company_id,
            event_type="APPLICATION_CREATED",
            created_at=timestamp,
            updated_at=timestamp,
            is_deleted=False,
            is_archived=False,
        )
        
        return event
    
    @staticmethod
    def create_interview_event(interview):
        """
        Crée un évènement pour un nouvel entretien
        """
        from apps.events.models import Event

        timestamp = int(time.time() * 1000)

        event = Event.objects.create(
            id=str(uuid.uuid4()),
            user=interview.user,
            title=f"Entretien - {interview.title or 'Sans titre'}",
            description=f"Entretien pour {interview.company_name or interview.company.name}",
            event_ts=interview.interview_ts,
            duration_minutes=interview.duration_minutes or 60,
            application_id=interview.application_id,
            company_id=interview.company_id,
            event_type="INTERVIEW_SCHEDULED",
            created_at=timestamp,
            updated_at=timestamp,
            is_deleted=False,
            is_archived=False
        )
        
        return event
    
    @staticmethod
    def create_call_event(call):
        """
        Crée un évènement pour un nouvel appel
        """
        from apps.events.models import Event

        timestamp = int(time.time() * 1000)
        company_name = call.company_name if hasattr(call, 'company_name') else (call.company.name if call.company else "Entreprise")

        event = Event.objects.create(
            id=str(uuid.uuid4()),
            user=call.user,
            title=f"Appel - {call.title or 'Sans titre'}",
            description=f"Appel avec {company_name}",
            event_ts=call.call_ts,
            duration_minutes=call.duration_minutes or 15,
            application_id=call.application_id,
            company_id=call.company_id,
            event_type="CALL_RECORDED",
            created_at=timestamp,
            updated_at=timestamp,
            is_deleted=False,
            is_archived=False
        )

        return event
    
    @staticmethod
    def create_followup_event(followup):
        """
        Crée un événement pour une nouvelle relance
        """
        from apps.events.models import Event

        timestamp = int(time.time() * 1000)
        event = Event.objects.create(
            id=str(uuid.uuid4()),
            user=followup.user,
            title=f"Relance - {followup.title or 'Sans titre'}",
            description=f"Relanec pour {followup.company_name or followup.company.name}",
            event_ts=followup.followup_ts,
            duration_minutes=30,
            application_id=followup.application_id,
            company_id=followup.company_id,
            event_type="FOLLOWUP_CREATED",
            created_at=timestamp,
            updated_at=timestamp,
            is_deleted=False,
            is_archived=False
        )

        return event