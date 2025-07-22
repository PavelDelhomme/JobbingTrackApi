from django.db import models
from apps.common.models.base import BaseModel

class Application(BaseModel):
    title            = models.CharField(max_length=255)
    company          = models.ForeignKey(
        'companies.Company',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='applications'
    )
    company_name     = models.CharField(max_length=255)      # accès rapide
    application_ts   = models.BigIntegerField()              # timestamp
    location         = models.CharField(max_length=255, blank=True)

    # références
    platform = models.ForeignKey(
        'applications.ApplicationPlatform', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='applications'
    )
    status = models.ForeignKey(
        'applications.ApplicationStatus', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='applications'
    )
    type = models.ForeignKey(
        'applications.ApplicationType',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='applications'
    )
    contract = models.ForeignKey(
        'applications.ApplicationContract',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='applications'
    )
    contract_type  = models.ForeignKey(
        'applications.ApplicationContractType',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='applications'
    )
    position  = models.ForeignKey(
        'applications.ApplicationPosition',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='applications'
    )
    department = models.ForeignKey(
        'applications.ApplicationDepartment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='applications'
    )

    # relations (listes d’IDs)
    contact_ids   = models.JSONField(default=list, blank=True)
    followup_ids  = models.JSONField(default=list, blank=True)
    interview_ids = models.JSONField(default=list, blank=True)
    call_ids      = models.JSONField(default=list, blank=True)
    event_ids     = models.JSONField(default=list, blank=True)

    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'applications'
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'
    
    def __str__(self):
        return f"{self.title} ({self.company_name})"

class ApplicationPlatform(BaseModel):
    name = models.CharField(max_length=255)
    class Meta:
        db_table = 'application_platforms'
        verbose_name = 'Application Platform'
        verbose_name_plural = 'Application Platforms'


class ApplicationStatus(BaseModel):
    name = models.CharField(max_length=255)
    class Meta:
        db_table = 'application_statuses'
        verbose_name = 'Application Status'
        verbose_name_plural = 'Application Statuses'


class ApplicationType(BaseModel):
    name = models.CharField(max_length=255)
    class Meta:
        db_table = 'application_types'
        verbose_name = 'Application Type'
        verbose_name_plural = 'Application Types'
    

class ApplicationContract(BaseModel):
    name = models.CharField(max_length=255)
    class Meta:
        db_table = 'application_contracts'
        verbose_name = 'Application Contract'
        verbose_name_plural = 'Application Contracts'

class ApplicationContractType(BaseModel):
    name = models.CharField(max_length=255)
    class Meta:
        db_table = 'application_contract_types'
        verbose_name = 'Application Contract Type'
        verbose_name_plural = 'Application Contract Types'


class ApplicationDepartment(BaseModel):
    name = models.CharField(max_length=255)
    class Meta:
        db_table = 'application_departments'
        verbose_name = 'Application Department'
        verbose_name_plural = 'Application Departments'

class ApplicationPosition(BaseModel):
    name = models.CharField(max_length=255)
    class Meta:
        db_table = 'application_positions'
        verbose_name = 'Application Position'
        verbose_name_plural = 'Application Positions'