#backend/api/appels/models.py
from django.db import models
from api.common.models.base import BaseModel
from django.utils import timezone
import datetime

class Call(BaseModel):   
    # Champs métier
    date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    duree_minutes = models.IntegerField(null=True, blank=True)
    resume = models.TextField(null=True, blank=True)
    call_type = models.ForeignKey("CallType", on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.CharField(max_length=255)
    notes = models.TextField(null=True, blank=True)
    
    # Liens obligatoires
    company_id = models.UUIDField(db_index=True, null=True, blank=True)
    application_id = models.UUIDField(db_index=True, null=True, blank=True)

    # Liens facultatifs
    contact_id = models.UUIDField(null=True, blank=True)
    followup_id = models.UUIDField(null=True, blank=True)
    
    @property
    def user(self):
        from api.common.models import UserCall
        user_call = UserCall.objects.filter(call_id=self.id).first()
        return user_call.user_id if user_call else None
    
    @property
    def company(self):
        from api.common.models import CompanyCall
        company_call = CompanyCall.objects.filter(call_id=self.id).first()
        return company_call.company_id if company_call else None
    
    
    def __str__(self):
        return f"Appel le {self.date.strftime('%d/%m/%Y %H:%M')}"

class CallType(BaseModel):
    type = models.CharField(max_length=100)
    
    def __str__(self):
        return self.type