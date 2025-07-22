from django.db import models
from apps.common.models.base import BaseModel
from apps.applications.models import Application
from apps.calendar.models import Calendar
from apps.events.models import Event
from apps.calls.models import Call
from apps.companies.models import Company
from apps.contacts.models import Contact
from apps.cvs.models import Cv
from apps.followups.models import FollowUp
from apps.interviews.models import Interview

class Note(BaseModel):
    title = models.CharField(max_length=255)
    content = models.TextField()

    class Meta:
        db_table = 'notes'
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'

    def __str__(self):
        return self.title

class Project(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        db_table = 'projects'
        verbose_name = 'Projet'
        verbose_name_plural = 'Projets'

    def __str__(self):
        return self.title

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
    
    # Autres champs
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    timezone = models.CharField(max_length=50, default='Europe/Paris')
    notes = models.TextField(blank=True)
    
    # Stats
    apps_last_7 = models.PositiveIntegerField(default=0, editable=False)
    calls_last_7 = models.PositiveIntegerField(default=0, editable=False)
    fu_last_7 = models.PositiveIntegerField(default=0, editable=False)
    itw_last_7 = models.PositiveIntegerField(default=0, editable=False)
    contacts_last_7 = models.PositiveIntegerField(default=0, editable=False)

    # Listes d'IDs centralisées pour l'utilisateur
    @property
    def applications(self):
        return Application.objects.filter(user=self.user)
    @property
    def calendars(self):
        return Calendar.objects.filter(user=self.user)
    @property
    def events(self):
        return Event.objects.filter(user=self.user)
    @property
    def calls(self):
        return Call.objects.filter(user=self.user)
    @property
    def companies(self):
        return Company.objects.filter(user=self.user)
    @property
    def contacts(self):
        return Contact.objects.filter(user=self.user)
    @property
    def cvs(self):
        return Cv.objects.filter(user=self.user)
    @property
    def followups(self):
        return FollowUp.objects.filter(user=self.user)
    @property
    def interviews(self):
        return Interview.objects.filter(user=self.user)
    @property
    def notes(self):
        return Note.objects.filter(user=self.user)
    @property
    def projects(self):
        return Project.objects.filter(user=self.user)

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