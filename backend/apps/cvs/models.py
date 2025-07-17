from apps.common.models.base import BaseModel
from django.db import models

class Cv(BaseModel):
    """CV principal d'un utilisateur"""
    title = models.CharField(max_length=255)
    summary = models.TextField(blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='cvs')

    def __str__(self):
        return f"CV {self.title} ({self.user})"

class Education(BaseModel):
    """Formation académique"""
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE, related_name='educations')
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    description = models.TextField(blank=True)

class Experience(BaseModel):
    """Expérience professionnelle"""
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE, related_name='experiences')
    company = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

class Skill(BaseModel):
    """Compétence technique ou langages"""
    name = models.CharField(max_length=100)
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE, related_name='skills')
    level = models.CharField(max_length=20, choices=(
        ('BEGINNER', 'Débutant'),
        ('INTERMEDIATE', 'Intermédiaire'),
        ('ADVANCED', 'Avancé'),
        ('EXPERT', 'Expert')
    ))
