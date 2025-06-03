from django.db import models
from common.models.base import BaseModel

class Profile(BaseModel):
    user_id = models.UUIDField(db_index=True)
    subject = models.CharField(max_length=255)
    skills = models.JSONField(default=list, blank=True)
    notes = models.TextField(null=True, blank=True)

    company_ids = models.JSONField(default=list, blank=True)
    contact_ids = models.JSONField(default=list, blank=True)
    candidature_ids = models.JSONField(default=list, blank=True)
    relance_ids = models.JSONField(default=list, blank=True)


class Language(BaseModel):
    user_id = models.UUIDField()
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='languages')
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=100)
    certification = models.CharField(max_length=255, null=True, blank=True)

class Experience(BaseModel):
    user_id = models.UUIDField()
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='experiences')
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

class Education(BaseModel):
    user_id = models.UUIDField()
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='educations')
    diploma = models.CharField(max_length=255)
    school = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

class Project(BaseModel):
    user_id = models.UUIDField()
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    description = models.TextField()

class CV(BaseModel):
    user_id = models.UUIDField(db_index=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='cvs')
    file = models.FileField(upload_to='cvs/')
