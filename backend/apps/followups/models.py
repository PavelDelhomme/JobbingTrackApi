from apps.common.models.base import BaseModel
from django.db import models

class FollowUp(BaseModel):
    title = models.CharField(max_length=255, blank=True)
    followup_ts     = models.BigIntegerField() # Timestamp de la relance

    # Relations obligatoires
    application_id  = models.CharField(max_length=36)
    company_id      = models.CharField(max_length=36)
    
    # Relations optionnelles
    contact_id      = models.CharField(max_length=36, null=True, blank=True)
    # appel créé automatiquement ?
    call_id         = models.CharField(max_length=36, null=True, blank=True) # Si relance par téléphone

    # Références
    platform_ref_id = models.CharField(max_length=36, null=True, blank=True)
    type_ref_id     = models.CharField(max_length=36)
    status_ref_id   = models.CharField(max_length=36, null=True, blank=True)
    
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
