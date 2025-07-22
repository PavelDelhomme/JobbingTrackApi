from apps.common.models.base import BaseModel
from django.db import models

class Call(BaseModel):
    title           = models.CharField(max_length=255)
    call_ts         = models.BigIntegerField()                 # timestamp
    company_id       = models.ForeignKey('companies.Company', on_delete=models.SET_NULL, null=True, blank=True)
    company_name    = models.CharField(max_length=255, blank=True)
    contact_id      = models.ForeignKey('contacts.Contact', on_delete=models.SET_NULL, null=True, blank=True)
    contact_name    = models.CharField(max_length=255, blank=True)

    # si l’appel crée une candidature
    #application_id  = models.CharField(max_length=36, null=True, blank=True)
    application_id = models.ForeignKey('applications.Application', on_delete=models.SET_NULL, null=True, blank=True)

    #call_type_ref_id = models.CharField(max_length=36, null=True, blank=True)
    call_type_ref_id = models.ForeignKey('calls.CallType', on_delete=models.SET_NULL, null=True, blank=True)
    notes            = models.TextField(blank=True)

    class Meta:
        db_table = 'calls'
        verbose_name = 'Call'
        verbose_name_plural = 'Calls'
    
    def __str__(self):
        return self.title