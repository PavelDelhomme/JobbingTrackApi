from django.db import models
from apps.common.models.base import BaseModel

class Calendar(BaseModel):
    name = models.CharField(max_length=255, default='Calendrier principal')
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#3498db')  # Couleur hex
    is_default = models.BooleanField(default=True)
    
    # Les events seront liés via leur event_ids - pas besoin de stocker ici
    # car chaque Event a déjà un user et on peut filtrer par user
    
    # Paramètres de vue
    default_view = models.CharField(max_length=20, default='MONTH')  # DAY, WEEK, MONTH
    
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'calendars'
        verbose_name = 'Calendar'
        verbose_name_plural = 'Calendars'
    
    def __str__(self):
        return f"{self.name} ({self.user.email})"
