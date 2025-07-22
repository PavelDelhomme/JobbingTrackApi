from apps.common.models.base import BaseModel
from django.db import models

class FollowUp(BaseModel):
    title = models.CharField(max_length=255, blank=True)
    followup_ts     = models.BigIntegerField() # Timestamp de la relance

    # Relations obligatoires avec ForeignKey
    application = models.ForeignKey(
        'applications.Application',
        on_delete=models.CASCADE,
        related_name='followups'
    )
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,
        related_name='followups'
    )
    
    # Relations optionnelles avec ForeignKey
    contact = models.ForeignKey(
        'contacts.Contact',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='followups'
    )
    call = models.ForeignKey(
        'calls.Call',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='followups'
    )
    
    # Références avec ForeignKey
    platform = models.ForeignKey(
        'references.Reference',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='followups_by_platform'
    )
    type = models.ForeignKey(
        'references.Reference',
        on_delete=models.SET_NULL,
        null=True,
        related_name='followups_by_type'
    )
    status = models.ForeignKey(
        'references.Reference',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='followups_by_status'
    )
    
    # Détails de la relance
    method = models.CharField(max_length=50, default='EMAIL') # EMAIL, PHONE, LINKEDIN, etc.
    response_received = models.BooleanField(default=False)
    next_followup_ts = models.BigIntegerField(null=True, blank=True) # Prochaine relance prévue
    notes           = models.TextField(blank=True)

    class Meta:
        db_table = 'followups'
        verbose_name = 'FollowUp'
        verbose_name_plural = 'FollowUps'
    
    def __str__(self):
        return f"Relance - ${self.title or 'Sans titre'}"
