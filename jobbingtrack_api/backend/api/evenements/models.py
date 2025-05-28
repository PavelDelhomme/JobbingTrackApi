from django.db import models
from common.models.base import BaseModel
from users.models import User

class Event(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    related_object_id = models.UUIDField(null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    type = models.CharField(max_length=100)
