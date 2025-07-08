from django.db import models
from api.common.models.base import BaseModel

class FollowUp(BaseModel):
    application_id = models.UUIDField()
    company_id = models.UUIDField()
    call_id = models.UUIDField(null=True, blank=True)
    event_id = models.UUIDField(null=True, blank=True)
    date = models.DateTimeField()
    message = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=100)
    notes = models.TextField(null=True, blank=True)
