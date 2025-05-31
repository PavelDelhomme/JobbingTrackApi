from django.db import models
from common.models.base import BaseModel

class Contact(BaseModel):
    user_id = models.UUIDField(db_index=True)

    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    position = models.CharField(max_length=255, null=True, blank=True)
    department = models.CharField(max_length=255, null=True, blank=True)

    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name or ''} {self.last_name or ''}".strip()

    class Meta:
        indexes = [
            models.Index(fields=["user_id"]),
            models.Index(fields=["email"]),
        ]
