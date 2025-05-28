from django.db import models
from common.models.base import BaseModel
from users.models import User

class Entretien(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    candidature = models.ForeignKey("candidatures.Candidature", on_delete=models.CASCADE)
    company = models.ForeignKey("entreprises.Entreprise", on_delete=models.CASCADE)
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
