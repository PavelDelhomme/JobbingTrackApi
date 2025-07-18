from django.db import models
from apps.common.models.base import BaseModel

class ReferenceType(models.TextChoices):
    # Applications
    APPLICATION_PLATFORM = 'APPLICATION_PLATFORM', 'Plateforme de candidature'
    APPLICATION_STATUS = 'APPLICATION_STATUS', 'Statut de candidature'
    APPLICATION_TYPE = 'APPLICATION_TYPE', 'Type de candidature'
    CONTRACT_TYPE = 'CONTRACT_TYPE', 'Type de contrat'
    
    # Calls
    CALL_TYPE = 'CALL_TYPE', 'Type d\'appel'
    
    # Followups
    FOLLOWUP_TYPE = 'FOLLOWUP_TYPE', 'Type de relance'
    FOLLOWUP_STATUS = 'FOLLOWUP_STATUS', 'Statut de relance'
    FOLLOWUP_PLATFORM = 'FOLLOWUP_PLATFORM', 'Plateforme de relance'
    
    # Interviews
    INTERVIEW_TYPE = 'INTERVIEW_TYPE', 'Type d\'entretien'
    INTERVIEW_STATUS = 'INTERVIEW_STATUS', 'Statut d\'entretien'
    INTERVIEW_STYLE = 'INTERVIEW_STYLE', 'Style d\'entretien'
    
    # Events
    EVENT_TYPE = 'EVENT_TYPE', 'Type d\'événement'
    
    # Companies
    COMPANY_TYPE = 'COMPANY_TYPE', 'Type d\'entreprise'
    COMPANY_SIZE = 'COMPANY_SIZE', 'Taille d’entreprise'
    COMPANY_LEGAL = 'COMPANY_LEGAL', 'Forme juridique'
    CONTACT_SENIORITY = 'CONTACT_SENIORITY', 'Niveau hiérarchique'

    # Contacts
    DEPARTMENT_TYPE = 'DEPARTMENT_TYPE', 'Type de département'
    POSITION_TYPE = 'POSITION_TYPE', 'Type de poste'

class Reference(BaseModel):
    """Modèle générique pour toutes les références/types"""
    label = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=ReferenceType.choices)
    description = models.TextField(blank=True)
    is_default = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'references'
        unique_together = ['user', 'label', 'type']
        verbose_name = 'Référence'
        verbose_name_plural = 'Références'
    
    def __str__(self):
        return f"{self.get_type_display()} - {self.label}"
