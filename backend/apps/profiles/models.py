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
    
    # Stats mises à jour par ProfileService (pas éditables dans l’admin)
    apps_last_7  = models.PositiveIntegerField(default=0, editable=False)
    calls_last_7 = models.PositiveIntegerField(default=0, editable=False)
    fu_last_7    = models.PositiveIntegerField(default=0, editable=False)
    itw_last_7   = models.PositiveIntegerField(default=0, editable=False)
    contacts_last_7 = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
    
    def __str__(self):
        return f"Profil de {self.user.email}"


class UserSettings(BaseModel):
    """
    Préférences UI et notifications et utilisateur.
    """
    profile = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name='settings'
    )
    theme = models.CharField(max_length=15, default='SYSTEM')
    timezone = models.CharField(max_length=50, default='Europe/Paris')
    notif_email = models.BooleanField(default=True)
    notif_push = models.BooleanField(default=True)
    dashboard_range = models.IntegerField(default=7) # nb de jours par défaut

    class Meta:
        db_table = 'user_settings'
        verbose_name = 'Settings'
        verbose_name_plural = 'Settings'