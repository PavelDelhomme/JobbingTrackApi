from django.db import models

from common.models.base import BaseModel

class Candidature(BaseModel):
    user = models.ForeignKey("authentication.User", on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    company = models.ForeignKey("entreprises.Entreprise", on_delete=models.SET_NULL)
    application_date = models.DateTimeField()
    platform = models.CharField(max_length=100, null=True, blank=True)
    contract_type = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    application_type = models.CharField(max_length=255)
    application_status = models.CharField(max_length=255)
    notes = models.TextField(null=True, blank=True)

class CandidatureContact(models.Model):
    candidature = models.ForeignKey("candidatures.Candidature", on_delete=models.SET_NULL)
    contact = models.ForeignKey("contacts.Contact", on_delete=models.SET_NULL)

    class Meta:
        unique_together = ("candidature", "contact")