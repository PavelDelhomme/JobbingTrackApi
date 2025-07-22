from django.db import transaction
from django.db import models
import uuid
import time
from apps.common.models.sync import SyncLedger
from apps.applications.models import Application
from apps.companies.models import Company
from apps.events.models import Event

class ApplicationService:
    @staticmethod
    @transaction.atomic
    def create_or_update_application(data, user):
        """
        Crée ou met à jour une candidature avec gestion des entités liées
        """
        # Vérifier si la company existe, sinon la créer
        company_id = data.get('company_id')
        company_name = data.get('company_name')

        company = None
        if company_id:
            try:
                from apps.companies.models import Company
                company = Company.objects.get(id=company_id, user=user)
            except Company.DoesNotExist:
                pass
        
        # Si pas de company trouvée mais un nom fourni, créer une nouvelle company
        if not company and company_name:
            from apps.companies.services import CompanyService
            company = CompanyService.create_minimal_company(company_name, user)
            data['companyç_id'] = str(company.id)
        
        # Créer ou mettre à jour l'application via le SyncService
        from apps.common.sync import SyncService
        application, created = SyncService.update_from_client(
            'applications.Application',
            data,
            user
        )

        # Créer un évènement pour cette candidature
        if created:
            from apps.events.services import EventService
            EventService.create_application_event(application)
        
        return application, created


    def create_initial_events(application):
        # Event « Candidature envoyée »
        Event.objects.create(
            user=application.user,
            title=f"Candidature : {application.title}",
            event_type_ref_id='EVENT_TYPE_APPLICATION_SENT',
            start_ts=application.application_ts,
            related_object_id=application.id,
            related_object_type='APPLICATION',
        )
        # Event de relance automatique J+7
        Event.objects.create(
            user=application.user,
            title=f"Relance – {application.title}",
            event_type_ref_id='EVENT_TYPE_FOLLOWUP_REMINDER',
            start_ts=application.application_ts + 7*24*3600,
            related_object_id=application.id,
            related_object_type='APPLICATION',
            notification_enabled=True,
        )
        
        # Mise à jour de la liste dans Company
        Company.objects.filter(pk=application.company_id).update(
            application_ids=models.F('application_ids') + [application.id]
        )

    @staticmethod
    def update_events(application, old_ts):
        """Si la date change → on décale les événements liés."""
        if application.application_ts == old_ts:
            return
        for ev in Event.objects.filter(
            related_object_id=application.id,
            related_object_type='APPLICATION'
        ):
            delta = application.application_ts - old_ts
            ev.start_ts += delta
            if ev.end_ts:
                ev.end_ts += delta
            ev.save(update_fields=['start_ts', 'end_ts'])
            
    
    def on_create(app):
        Event.objects.create(
            user               = app.user,
            title              = f"Candidature envoyée – {app.title}",
            event_type_ref_id  = 'EVENT_TYPE_APPLICATION_SENT',
            start_ts           = app.application_ts,
            related_object_id  = app.id,
            related_object_type= 'APPLICATION',
        )
        # Relance automatique J+7
        Event.objects.create(
            user              = app.user,
            title             = f"Relance – {app.title}",
            event_type_ref_id = 'EVENT_TYPE_FOLLOWUP_REMINDER',
            start_ts          = app.application_ts + 7*24*3600,
            related_object_id = app.id,
            related_object_type='APPLICATION',
            notification_enabled = True,
        )

    @staticmethod
    def on_update(app, old_ts):
        if app.application_ts != old_ts:
            delta = app.application_ts - old_ts
            Event.objects.filter(
                related_object_id=app.id,
                related_object_type='APPLICATION'
            ).update(start_ts=models.F('start_ts') + delta)
