from django.db import models
import uuid
import uuid
from django.db import models
from django.conf import settings


class BaseModel(models.Model):
    """
    Champ id string (uuid4), dates et soft-delete.
    """
    id = models.CharField(primary_key=True,
                          max_length=36,
                          default=uuid.uuid4,
                          editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='%(class)s_objects')
    sync_hash = models.CharField(max_length=128)
    is_archived = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    archived_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)
