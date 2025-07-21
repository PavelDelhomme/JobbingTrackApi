from django.db import models
from apps.profiles.models import UserProfile

class CvService:
    @staticmethod
    def ensure_single_primary(cv):
        if cv.is_primary:
            cv.__class__.objects.filter(user=cv.user, is_primary=True)\
                .exclude(pk=cv.pk).update(is_primary=False)
    
    @staticmethod
    def on_create(cv):
        UserProfile.objects.filter(user=cv.user).update(
            cv_ids=models.F("cv_ids") + [cv.id]
        )
        CvService.ensure_single_primary(cv)
    
    
    @staticmethod
    def on_update(cv):
        CvService.ensure_single_primary(cv)