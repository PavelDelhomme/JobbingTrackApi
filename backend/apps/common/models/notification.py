from django.db import models
from django.conf import settings

class PushNotification(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    data = models.JSONField(default=dict)
    created_at = models.BigIntegerField()
    is_read = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'push_notifications'
        verbose_name = 'Notification Push'
        verbose_name_plural = 'Notifications Push'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title