from django.db import models
from common.models.base import BaseModel

class Contact(BaseModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
