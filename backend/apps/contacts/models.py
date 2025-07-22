from django.db import models
from apps.common.models.base import BaseModel

class Contact(BaseModel):
    first_name  = models.CharField(max_length=255)
    last_name   = models.CharField(max_length=255)
    email       = models.EmailField(blank=True)
    phone       = models.CharField(max_length=50, blank=True)

    # Relations avec ForeignKey
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contacts"
    )
    company_name = models.CharField(max_length=255, blank=True) # Pour un accès rapide

    # Références avec ForeignKey
    position = models.ForeignKey(
        'references.Reference',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contacts_by_position'
    )
    department = models.ForeignKey(
        'references.Reference',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contacts_by_department'
    )
    contract_type = models.ForeignKey(
        'references.Reference',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contacts_by_contract_type'
    )
    
    # liaisons
    application_ids = models.JSONField(default=list, blank=True)
    followup_ids    = models.JSONField(default=list, blank=True)
    interview_ids   = models.JSONField(default=list, blank=True)
    call_ids        = models.JSONField(default=list, blank=True)
    event_ids       = models.JSONField(default=list, blank=True)

    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'contacts'
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
