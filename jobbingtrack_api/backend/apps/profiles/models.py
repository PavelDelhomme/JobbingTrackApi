#backend/api/profiles/models.py
from django.db import models
from api.common.models.base import BaseModel

class Profile(BaseModel):
    subject = models.CharField(max_length=255)
    skills = models.JSONField(default=list, blank=True)
    notes = models.TextField(null=True, blank=True)

    company_ids = models.JSONField(default=list, blank=True)
    contact_ids = models.JSONField(default=list, blank=True)
    application_ids = models.JSONField(default=list, blank=True)
    followup_ids = models.JSONField(default=list, blank=True)
    interview_ids = models.JSONField(default=list, blank=True)
    call_ids = models.JSONField(default=list, blank=True)


class Language(BaseModel):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='languages')
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=100)
    certification = models.CharField(max_length=255, null=True, blank=True)

class Experience(BaseModel):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='experiences')
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

class Education(BaseModel):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='educations')
    diploma = models.CharField(max_length=255)
    school = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

class Project(BaseModel):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    description = models.TextField()

class CV(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='cvs')
    file = models.FileField(upload_to='cvs/')
