from django.db import models
from common.models.base import BaseModel

class Relance(BaseModel):
    candidature_id = models.UUIDField()
    entreprise_id = models.UUIDField()
    appel_id = models.UUIDField(null=True, blank=True)
    event_id = models.UUIDField(null=True, blank=True)
    date = models.DateTimeField()
    message = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=100)
    notes = models.TextField(null=True, blank=True)
