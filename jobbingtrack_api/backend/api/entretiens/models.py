from django.db import models
from common.models.base import BaseModel

class Entretien(BaseModel):
    user_id = models.UUIDField(db_index=True)
    candidature_id = models.UUIDField()
    entreprise_id = models.UUIDField()

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
