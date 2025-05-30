from django.db import models
from common.models.base import BaseModel

class Profile(BaseModel):
    user_id = models.UUIDField(db_index=True)  # lien utilisateur
    subject = models.CharField(max_length=255)
    company_ids = models.TextField()
    contact_ids = models.TextField(null=True, blank=True)
    candidature_ids = models.TextField(null=True, blank=True)
    relance_ids = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
