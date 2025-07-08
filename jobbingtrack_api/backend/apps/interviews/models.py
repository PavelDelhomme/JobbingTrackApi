#backend/api/entretiens/models.py
from django.db import models
from api.common.models.base import BaseModel

    
class Interview(BaseModel):
    application_id = models.UUIDField(db_index=True)
    company_id = models.UUIDField(db_index=True)

    date_time = models.DateTimeField()
    duration_minutes = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    style = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)

    pre_interview_notes = models.TextField(null=True, blank=True)
    interview_notes = models.TextField(null=True, blank=True)
    post_interview_notes = models.TextField(null=True, blank=True)

    return_date = models.DateTimeField(null=True, blank=True)
    tests_needed = models.BooleanField(default=False)
    tests_deadline = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Entretien {self.id} - {self.date_time}"