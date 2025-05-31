from django.db import models
from common.models.base import BaseModel

class Event(BaseModel):
    user_id = models.UUIDField(db_index=True)
    related_object_id = models.UUIDField(null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    type = models.CharField(max_length=100)
