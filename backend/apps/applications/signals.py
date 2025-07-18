from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from apps.applications.models import Application
from apps.companies.models import Company

@receiver(pre_save, sender=Application)
def auto_create_company(sender, instance, **kwargs):
    if instance.company_id:
        return # Déà lié a une entreprise existante
    company, _ = Company.objects.get_or_create(
        name=instance.company_name,
        user=instance.user
    )
    instance.company_id = company.id
    

@receiver(pre_save, sender=Application)
def ensure_company(sender, instance, **kwargs):
    """
    Crée ou met à jour Company avant d’enregistrer l’application.
    - Si instance.company_id existe -> on vérifie seulement le renommage.
    - Sinon on crée la société et on injecte l’ID.
    """
    if instance.company_id:
        # Vérifier un éventuel renommage
        try:
            company = Company.objects.get(pk=instance.company_id, user=instance.user)
            if company.name != instance.company_name:
                company.name = instance.company_name
                company.save(update_fields=["name"])
        except Company.DoesNotExist:
            pass
    else:
        company, _ = Company.objects.get_or_create(
            name=instance.company_name,
            user=instance.user,
            defaults={"sector": "", "notes": ""}
        )
        instance.company_id = company.id