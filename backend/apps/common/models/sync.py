from django.db import models
from django.conf import settings

class SyncLedger(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=120) # ex : applications.application
    last_synced = models.DateTimeField(auto_now=True)
    last_hash = models.CharField(max_length=128, blank=True)
    
    class Meta:
        unique_together = ('user', 'model_name')