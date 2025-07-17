from django.db import models
from apps.common.models.base import BaseModel


class Event(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    event_type_ref_id = models.CharField(max_length=36)
    
    start_ts = models.BigIntegerField()  # Timestamp de début
    end_ts = models.BigIntegerField(null=True, blank=True)  # Timestamp de fin
    
    # Objet lié (candidature, appel, entretien, relance)
    related_object_id = models.CharField(max_length=36)
    related_object_type = models.CharField(max_length=50)  # APPLICATION, CALL, INTERVIEW, FOLLOWUP
    
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