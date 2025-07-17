from django.db import models
from apps.common.models.base import BaseModel

class Company(BaseModel):
    name          = models.CharField(max_length=255)
    type_ref_id   = models.CharField(max_length=36, null=True, blank=True)
    sector        = models.CharField(max_length=255, blank=True)
    website       = models.URLField(blank=True)
    address       = models.TextField(blank=True)
    phone         = models.CharField(max_length=50, blank=True)
    email         = models.EmailField(blank=True)

    # Relations (listes d'IDs)
    contact_ids     = models.JSONField(default=list, blank=True)
    application_ids = models.JSONField(default=list, blank=True)
    followup_ids    = models.JSONField(default=list, blank=True)
    interview_ids   = models.JSONField(default=list, blank=True)
    call_ids        = models.JSONField(default=list, blank=True)
    event_ids       = models.JSONField(default=list, blank=True)

    notes           = models.TextField(blank=True)

    class Meta:
        db_table = 'companies'
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
    
    def __str__(self):
        return self.name
