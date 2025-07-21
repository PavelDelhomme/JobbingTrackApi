from apps.common.models.base import BaseModel
from django.db import models

class Cv(BaseModel):
    """CV principal d'un utilisateur"""
    title = models.CharField(max_length=255)
    summary = models.TextField(blank=True)
    file_path = models.CharField(max_length=500, blank=True) # Chemin vers le fichier PDF
    is_primary = models.BooleanField(default=False) # CV principal

    # Relation avec les éléments du CV
    education_ids = models.JSONField(default=list, blank=True)
    experience_ids = models.JSONField(default=list, blank=True)
    skill_ids = models.JSONField(default=list, blank=True)
    language_ids = models.JSONField(default=list, blank=True)
    project_ids = models.JSONField(default=list, blank=True)
    certification_ids = models.JSONField(default=list, blank=True)

    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'cvs'
        verbose_name = 'CV'
        verbose_name_plural = 'CVs'

    def __str__(self):
        return f"{self.title} ({'Principal' if self.is_primary else 'Secondaire'})"

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

class Language(BaseModel):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE, related_name='languages')
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=50, choices=(
        ('A1', 'A1'), ('A2', 'A2'), ('B1', 'B1'), ('B2', 'B2'), ('C1', 'C1'), ('C2', 'C2'), ('NATIVE', 'Natif')
    ))
    certified = models.BooleanField(default=False)
    certificate_name = models.CharField(max_length=255, blank=True)
    
class Project(BaseModel):
    """ Projet professionnel/personnel réalisé"""
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True)

class Certification(BaseModel):
    """Certification professionnelle/personnelle"""
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=255)
    authority = models.CharField(max_length=255, blank=True)
    date_obtained = models.DateField(null=True, blank=True)
    link = models.URLField(blank=True)