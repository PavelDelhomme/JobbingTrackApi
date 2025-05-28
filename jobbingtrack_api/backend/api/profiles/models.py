from django.db import models
from common.models.base import BaseModel
from users.models import User

class Profile(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    company_ids = models.TextField()
    contact_ids = models.TextField(null=True, blank=True)
    candidature_ids = models.TextField(null=True, blank=True)
    relance_ids = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
