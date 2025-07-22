from django.db import transaction

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
