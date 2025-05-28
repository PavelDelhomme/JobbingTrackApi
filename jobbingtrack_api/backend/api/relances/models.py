from django.db import models
from common.models.base import BaseModel

class Relance(BaseModel):
    user_id = models.UUIDField()
    candidature_id = models.UUIDField()
    entreprise_id = models.UUIDField()
    appel_id = models.UUIDField(null=True, blank=True)
    event_id = models.UUIDField(null=True, blank=True)
    date = models.DateTimeField()
    message = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=100)
    notes = models.TextField(null=True, blank=True)

class RelanceContact(models.Model):
    relance_id = models.UUIDField()
    contact_id = models.UUIDField()

    class Meta:
        unique_together = ("relance_id", "contact_id")
