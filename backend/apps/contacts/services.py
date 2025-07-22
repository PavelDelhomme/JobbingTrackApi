import uuid
import time
from django.db import transaction

class ContactService:

    @staticmethod
    @transaction.atomic
    def create_or_update_contact(data, user):
        """
        Crée ou met à jour un contact avec gestion des entités liées
        """
        # Vérifier si une entreprise est spécifiée ou doit être créée
        company_id = data.get('company_id')
        company_name = data.get('company_name')
        
        if not company_id and company_name:
            # Créer une nouvelle entreprise
            from apps.companies.services import CompanyService
            company = CompanyService.create_minimal_company(company_name, user)
            data['company_id'] = str(company.id)
        
        # Créer ou mettre à jour le contact
        from apps.common.sync import SyncService
        contact, created = SyncService.update_from_client(
            'contacts.Contact',
            data,
            user
        )
        
        return contact, created
    

    @staticmethod
    def create_minimal_contact(name, user, company_id=None, position='', email='', phone=''):
        """
        Crée un contact minimal
        """
        from apps.contacts.models import Contact
        
        # Séparer prénom/nom si possible
        name_parts = name.split(' ', 1)
        first_name = name_parts[0] if len(name_parts) > 0 else ''
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        # Créer le contact
        timestamp = int(time.time() * 1000)
        contact = Contact.objects.create(
            id=str(uuid.uuid4()),
            user=user,
            first_name=first_name,
            last_name=last_name,
            position=position,
            email=email,
            phone=phone,
            company_id=company_id,
            created_at=timestamp,
            updated_at=timestamp,
            is_deleted=False,
            is_archived=False
        )
        
        return contact