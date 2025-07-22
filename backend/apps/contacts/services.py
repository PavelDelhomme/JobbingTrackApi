import uuid
import time

class ContactService:
    @staticmethod
    def create_minimal_contact(name, user, company_id=None, position=''):
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
            company_id=company_id,
            created_at=timestamp,
            updated_at=timestamp,
            is_deleted=False,
            is_archived=False,
        )

        return contact