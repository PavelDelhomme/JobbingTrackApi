from django.db import models
import uuid
from common.models.base import BaseModel

class Contact(BaseModel):
    user_id = models.UUIDField(db_index=True)  # lien utilisateur
    
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    position = models.CharField(max_length=255, null=True, blank=True)
    department = models.CharField(max_length=255, null=True, blank=True)
    
    # Relations sous forme de listes d'UUIDs
    company_ids = models.JSONField(default=list, blank=True)        # entreprises liées
    candidature_ids = models.JSONField(default=list, blank=True)    # candidatures liées
    relance_ids = models.JSONField(default=list, blank=True)        # relances liées
    appel_ids = models.JSONField(default=list, blank=True)          # appels liés
    entretien_ids = models.JSONField(default=list, blank=True)      # entretiens liés

    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name or ''} {self.last_name or ''}".strip()

    class Meta:
        indexes = [
            models.Index(fields=["user_id"]),
            models.Index(fields=["email"]),
        ]