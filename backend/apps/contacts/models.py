from django.db import models
from apps.common.models.base import BaseModel

class Contact(BaseModel):
    first_name  = models.CharField(max_length=255)
    last_name   = models.CharField(max_length=255)
    email       = models.EmailField(blank=True)
    phone       = models.CharField(max_length=50, blank=True)

    company_id  = models.CharField(max_length=36, null=True, blank=True)
    company_name= models.CharField(max_length=255, blank=True)

    # Références
    position_ref_id = models.CharField(max_length=36, null=True, blank=True)
    department_ref_id = models.CharField(max_length=36, null=True, blank=True)
    contract_type_ref_id = models.CharField(max_length=36, null=True, blank=True)
    
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
