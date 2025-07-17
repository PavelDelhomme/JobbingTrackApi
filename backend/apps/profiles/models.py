from apps.common.models.base import BaseModel
from django.db import models

class UserProfile(BaseModel):
    """Vue centrale qui référence tout ce que possède l’utilisateur."""
    # listes d’IDs (JSONField) – on les remplira côté mobile/API
    application_ids = models.JSONField(default=list, blank=True)
    event_ids       = models.JSONField(default=list, blank=True)
    call_ids        = models.JSONField(default=list, blank=True)
    company_ids     = models.JSONField(default=list, blank=True)
    contact_ids     = models.JSONField(default=list, blank=True)
    cv_ids          = models.JSONField(default=list, blank=True)
    followup_ids    = models.JSONField(default=list, blank=True)
    interview_ids   = models.JSONField(default=list, blank=True)
    note_ids        = models.JSONField(default=list, blank=True)
    project_ids     = models.JSONField(default=list, blank=True)
    

    # Ex : infos complément-aires (bio, avatar...)
    bio   = models.TextField(blank=True)
    phone = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'Profil'
        verbose_name_plural = 'Profils'