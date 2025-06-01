from django.db import models
from common.models.base import BaseModel

class Appel(BaseModel):
    subject = models.CharField(max_length=255)
    entreprise_id = models.UUIDField(null=True, blank=True)
    candidature_id = models.UUIDField(null=True, blank=True)
    relance_id = models.UUIDField(null=True, blank=True)
    date_time = models.DateTimeField()
    notes = models.TextField(null=True, blank=True)
    
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