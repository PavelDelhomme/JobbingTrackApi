from django.db import models
from common.models.base import BaseModel

class Profile(BaseModel):
    user_id = models.UUIDField(db_index=True)
    subject = models.CharField(max_length=255)
    company_ids = models.JSONField(default=list, blank=True)
    contact_ids = models.JSONField(default=list, blank=True)
    candidature_ids = models.JSONField(default=list, blank=True)
    relance_ids = models.JSONField(default=list, blank=True)
    notes = models.TextField(null=True, blank=True)
