from django.db import models
from apps.companies.models import Company

class ContactService:
    @staticmethod
    def attach_company(contact):
        if contact.company_id:
            return
        if contact.company_name:
            comp, _ = Company.objects.get_or_create(
                user=contact.user,
                name=contact.company_name
            )
            contact.company_id = comp.id
            contact.save(update_fields=["company_id"])

            # Ajouter le contact à la liste de l'entreprise
            Company.objects.filter(pk=comp.id).update(
                contact_ids=models.F('contact_ids') + [contact.id]
            )
