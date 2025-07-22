from apps.common.models.base import BaseModel
from django.db import models

class Interview(BaseModel):
    title            = models.CharField(max_length=255, blank=True)
    interview_ts     = models.BigIntegerField()
    duration_minutes = models.IntegerField(null=True, blank=True)

    # Relations obligatoires
    application = models.ForeignKey(
        'applications.Application', 
        on_delete=models.CASCADE,
        related_name='interviews'
    )
    company = models.ForeignKey(
        'companies.Company', 
        on_delete=models.PROTECT,  # Empêche la suppression de l'entreprise si des entretiens existent
        related_name='interviews'
    )
    
    # Lieu et modalités
    location         = models.CharField(max_length=255, blank=True)
    is_remote        = models.BooleanField(default=False)
    meeting_link     = models.URLField(blank=True)

    # Références
    style_ref_id     = models.CharField(max_length=36, null=True, blank=True) # PHONE, VIDEO, FACE_TO_FACE
    type_ref_id      = models.CharField(max_length=36, null=True, blank=True) # TECHNICAL, HR, MANAGER
    status_ref_id    = models.CharField(max_length=36, null=True, blank=True) # SCHEDULED, COMPLETED, CANCELLED

    # Contacts présents (liste d'IDs)
    contact_ids      = models.JSONField(default=list, blank=True)

    # Notes
    notes_pre        = models.TextField(blank=True) # Notes avant l'entretien
    notes_during     = models.TextField(blank=True) # Notes pendant l'entretien
    notes_post       = models.TextField(blank=True) # Notes après l'entretien

    # Tests techniques
    tests_needed      = models.BooleanField(default=False)
    tests_done        = models.BooleanField(default=False)
    tests_deadline_ts = models.BigIntegerField(null=True, blank=True)

    # Suivi
    return_date_ts    = models.BigIntegerField(default=False) # Date de retour prévue
    salary_discussed  = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'interviews'
        verbose_name = 'Interview'
        verbose_name_plural = 'Interviews'
    
    def __str__(self):
        return f"Entretien - ${self.title or 'Sans titre'}"
