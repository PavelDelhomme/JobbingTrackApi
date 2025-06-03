from django.db import models
from common.models.base import BaseModel

class Candidature(BaseModel):
    entreprise_id = models.UUIDField(null=True, blank=True)

    title = models.CharField(max_length=255)
    candidature_date = models.DateTimeField()
    
    location = models.CharField(max_length=255, null=True, blank=True)
    plateforme = models.CharField(max_length=100, null=True, blank=True)
    contract_type = models.CharField(max_length=100, null=True, blank=True)
    
    notes = models.TextField(null=True, blank=True)
    
    candidature_type = models.CharField(max_length=100, choices=[
        ("SPONTANEOUS", "Spontanée"),
        ("OFFER", "Offre"),
    ])
    
    candidature_status = models.CharField(max_length=100, choices=[
        ("WAITING", "En attente"),
        ("TO_BE_FOLLOWED", "À relancer"),
        ("INTERVIEW_PENDING", "Entretien à venir"),
        ("REJECTED_WITHOUT_INTERVIEW", "Refus sans entretien"),
        ("REJECTED_AFTER_INTERVIEW", "Refus après entretien"),
    ])
    
    sync_hash = models.CharField(max_length=255)
    is_archived = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    archived_at = models.DateTimeField(null=True, blank=True)
    

    def __str__(self):
        return f"Candidature {self.title} ({self.id})"
