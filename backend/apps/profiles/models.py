from django.db import models
from apps.common.models.base import BaseModel

class UserProfile(BaseModel):
    # Informations personnelles complémentaires
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    
    # Préférences de recherche
    target_salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    target_salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    target_locations = models.JSONField(default=list, blank=True)  # Liste des lieux souhaités
    remote_work_preference = models.CharField(max_length=20, default='HYBRID')  # REMOTE, OFFICE, HYBRID
    
    # Listes d'IDs centralisées pour l'utilisateur
    application_ids = models.JSONField(default=list, blank=True)
    event_ids = models.JSONField(default=list, blank=True)
    call_ids = models.JSONField(default=list, blank=True)
    company_ids = models.JSONField(default=list, blank=True)
    contact_ids = models.JSONField(default=list, blank=True)
    cv_ids = models.JSONField(default=list, blank=True)
    followup_ids = models.JSONField(default=list, blank=True)
    interview_ids = models.JSONField(default=list, blank=True)
    note_ids = models.JSONField(default=list, blank=True)
    project_ids = models.JSONField(default=list, blank=True)
    
    # Paramètres de notification
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    
    # Paramètres généraux
    timezone = models.CharField(max_length=50, default='Europe/Paris')
    
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
    
    def __str__(self):
        return f"Profil de {self.user.email}"
