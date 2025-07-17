from apps.common.models.base import BaseModel
from django.db import models

class Calendar(BaseModel):
    name = models.CharField(max_length=255, default='Default')
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'calendars'
        verbose_name = 'Calendar'
        verbose_name_plural = 'Calendars'

    def __str__(self):
        return self.name
