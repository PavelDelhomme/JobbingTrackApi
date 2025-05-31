from django.db import models
from common.models.base import BaseModel

class Candidature(BaseModel):
    user_id = models.UUIDField()
    candidature_id = models.UUIDField()
    entreprise_id = models.UUIDField(null=True, blank=True)

    title = models.CharField(max_length=255)
    candidature_date = models.DateTimeField()
    platform = models.CharField(max_length=100, null=True, blank=True)
    contract_type = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    candidature_type = models.CharField(max_length=255)
    candidature_status = models.CharField(max_length=255)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Candidature {self.title} ({self.candidature_id})"
