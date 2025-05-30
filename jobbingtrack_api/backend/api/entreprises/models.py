from django.db import models
from common.models.base import BaseModel

class Entreprise(BaseModel):
    user_id = models.UUIDField(db_index=True)  # lien utilisateur
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    hr_email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)