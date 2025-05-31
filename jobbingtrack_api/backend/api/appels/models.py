from django.db import models
from common.models.base import BaseModel

class Appel(BaseModel):
    user_id = models.UUIDField()
    subject = models.CharField(max_length=255)
    entreprise_id = models.UUIDField(null=True, blank=True)
    candidature_id = models.UUIDField(null=True, blank=True)
    relance_id = models.UUIDField(null=True, blank=True)
    date_time = models.DateTimeField()
    notes = models.TextField(null=True, blank=True)
