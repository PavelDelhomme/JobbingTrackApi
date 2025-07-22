from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from apps.common.models.base import BaseModel


class Event(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Référence avec ForeignKey
    event_type = models.ForeignKey(
        'references.Reference',
        on_delete=models.SET_NULL,
        null=True,
        related_name='events'
    )
    
    start_ts = models.BigIntegerField()  # Timestamp de début
    end_ts = models.BigIntegerField(null=True, blank=True)  # Timestamp de fin
    
    # Relation générique (peut pointer vers n'importe quel modèle)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.CharField(max_length=36, null=True, blank=True)
    related_object = GenericForeignKey('content_type', 'object_id')
    
    # Pour compatibilité avec l'existant
    related_object_type = models.CharField(max_length=50, blank=True) # APPLICATION, FOLLOWUP, CALL
    
    # Paramètres de notification
    notification_enabled = models.BooleanField(default=True)
    notification_ts = models.BigIntegerField(null=True, blank=True)  # Quand notifier
    is_completed = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'events'
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
    
    def __str__(self):
        return f"{self.title} ({self.get_related_object_type_display()})"