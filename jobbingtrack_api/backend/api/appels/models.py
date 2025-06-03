from django.db import models
from common.models.base import BaseModel

class Appel(BaseModel):
    user_id = models.UUIDField(db_index=True)
    
    # Champs métier
    date = models.DateTimeField()
    duree_minutes = models.IntegerField(null=True, blank=True)
    resume = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)    
    subject = models.CharField(max_length=255)
    notes = models.TextField(null=True, blank=True)
    
    # Liens obligatoires
    entreprise_id = models.UUIDField(db_index=True)
    candidature_id = models.UUIDField(db_index=True)

    # Liens facultatifs
    contact_id = models.UUIDField(null=True, blank=True)
    relance_id = models.UUIDField(null=True, blank=True)
    
    @property
    def user(self):
        from common.models import UserAppel
        user_appel = UserAppel.objects.filter(appel_id=self.id).first()
        return user_appel.user_id if user_appel else None
    
    @property
    def entreprise(self):
        from common.models import EntrepriseAppel
        entreprise_appel = EntrepriseAppel.objects.filter(appel_id=self.id).first()
        return entreprise_appel.entreprise_id if entreprise_appel else None
    
    
    def __str__(self):
        return f"Appel le {self.date.strftime('%d/%m/%Y %H:%M')}"