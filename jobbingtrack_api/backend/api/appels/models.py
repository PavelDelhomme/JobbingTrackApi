from django.db import models
from common.models.base import BaseModel

class Appel(BaseModel):
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    company = models.ForeignKey("entreprises.Entreprise", on_delete=models.SET_NULL)
    contact = models.ForeignKey("contacts.Contact", null=True, blank=True, on_delete=models.SET_NULL)
    candidature = models.ForeignKey("candidatures.Candidature", null=True, blank=True, on_delete=models.SET_NULL)
    relance = models.ForeignKey("relances.Relance", null=True, blank=True, on_delete=models.SET_NULL)
    date_time = models.DateTimeField()
    notes = models.TextField(null=True, blank=True)