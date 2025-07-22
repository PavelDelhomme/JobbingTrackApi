import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
import time

class BaseModel(models.Model):
    """
    Modèle de base pour toutes les entités métier.
    Contient les champs communs : ID, user, sync, timestamps, soft delete
    """
    id = models.CharField(
        primary_key=True,
        max_length=36,
        default=uuid.uuid4,
        editable=False
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s_items'
    )
    
    sync_hash = models.CharField(max_length=128, blank=True)
    
    # Soft delete et archivage
    is_archived = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.BigIntegerField(default=lambda: int(time.time() * 1000))
    updated_at = models.BigIntegerField(default=lambda: int(time.time() * 1000))
    deleted_at = models.BigIntegerField(null=True, blank=True)
    archived_at = models.BigIntegerField(null=True, blank=True)
    
    class Meta:
        abstract = True
        ordering = ['-created_at']
    
    def soft_delete(self):
        """Suppression logique"""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
    
    def archive(self):
        """Archivage"""
        self.is_archived = True
        self.archived_at = timezone.now()
        self.save()
    
    def restore(self):
        """Restauration"""
        self.is_deleted = False
        self.is_archived = False
        self.deleted_at = None
        self.archived_at = None
        self.save()
