from django.db import models
from .base import BaseModel

class AbstractLinking(BaseModel):
    """
    Modèle abstrait pour les relations many-to-many personnalisées
    """
    class Meta:
        abstract = True

# Exemple d'utilisation pour les relations spécifiques
class ContactApplicationLink(AbstractLinking):
    """Relation entre Contact et Application"""
    contact_id = models.CharField(max_length=36)
    application_id = models.CharField(max_length=36)
    role = models.CharField(max_length=100, blank=True)  # Rôle du contact dans la candidature
    
    class Meta:
        unique_together = ['contact_id', 'application_id']
        db_table = 'contact_application_links'
