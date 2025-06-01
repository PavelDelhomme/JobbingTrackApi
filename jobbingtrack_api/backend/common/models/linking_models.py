from django.db import models

### CANDIDATURES RELATIONS ###
class CandidatureContact(models.Model):
    candidature_id = models.UUIDField()
    contact_id = models.UUIDField()
    class Meta:
        unique_together = ("candidature_id", "contact_id")

class CandidatureRelance(models.Model):
    candidature_id = models.UUIDField()
    relance_id = models.UUIDField()
    class Meta:
        unique_together = ("candidature_id", "relance_id")

class CandidatureAppel(models.Model):
    candidature_id = models.UUIDField()
    appel_id = models.UUIDField()
    class Meta:
        unique_together = ("candidature_id", "appel_id")

class CandidatureEntretien(models.Model):
    candidature_id = models.UUIDField()
    entretien_id = models.UUIDField()
    class Meta:
        unique_together = ("candidature_id", "entretien_id")

class CandidatureEntreprise(models.Model):
    candidature_id = models.UUIDField()
    entreprise_id = models.UUIDField()
    class Meta:
        unique_together = ("candidature_id", "entreprise_id")


### CONTACTS RELATIONS ###
class ContactEntreprise(models.Model):
    contact_id = models.UUIDField()
    entreprise_id = models.UUIDField()
    class Meta:
        unique_together = ("contact_id", "entreprise_id")

class ContactAppel(models.Model):
    contact_id = models.UUIDField()
    appel_id = models.UUIDField()
    class Meta:
        unique_together = ("contact_id", "appel_id")

class ContactEntretien(models.Model):
    contact_id = models.UUIDField()
    entretien_id = models.UUIDField()
    class Meta:
        unique_together = ("contact_id", "entretien_id")

class ContactRelance(models.Model):
    contact_id = models.UUIDField()
    relance_id = models.UUIDField()
    class Meta:
        unique_together = ("contact_id", "relance_id")


### ENTREPRISE RELATIONS ###
class EntrepriseAppel(models.Model):
    entreprise_id = models.UUIDField()
    appel_id = models.UUIDField()
    class Meta:
        unique_together = ("entreprise_id", "appel_id")

class EntrepriseRelance(models.Model):
    entreprise_id = models.UUIDField()
    relance_id = models.UUIDField()
    class Meta:
        unique_together = ("entreprise_id", "relance_id")

class EntrepriseEntretien(models.Model):
    entreprise_id = models.UUIDField()
    entretien_id = models.UUIDField()
    class Meta:
        unique_together = ("entreprise_id", "entretien_id")


### EVENTS RELATIONS ###
class CandidatureEvent(models.Model):
    event_id = models.UUIDField()
    candidature_id = models.UUIDField()
    class Meta:
        unique_together = ("event_id", "candidature_id")

class RelanceEvent(models.Model):
    event_id = models.UUIDField()
    relance_id = models.UUIDField()
    class Meta:
        unique_together = ("event_id", "relance_id")

class AppelEvent(models.Model):
    user_id = models.UUIDField(null=True, blank=True)
    event_id = models.UUIDField()
    appel_id = models.UUIDField()
    class Meta:
        unique_together = ("event_id", "appel_id")

class EntretienEvent(models.Model):
    event_id = models.UUIDField()
    entretien_id = models.UUIDField()
    class Meta:
        unique_together = ("event_id", "entretien_id")

class EntrepriseEvent(models.Model):
    event_id = models.UUIDField()
    entreprise_id = models.UUIDField()
    class Meta:
        unique_together = ("event_id", "entreprise_id")


### USER RELATIONS (liens profil / utilisateur) ###
class UserCandidature(models.Model):
    user_id = models.UUIDField()
    candidature_id = models.UUIDField()
    class Meta:
        unique_together = ("user_id", "candidature_id")

class UserAppel(models.Model):
    user_id = models.UUIDField()
    appel_id = models.UUIDField()
    class Meta:
        unique_together = ("user_id", "appel_id")

class UserEntretien(models.Model):
    user_id = models.UUIDField()
    entretien_id = models.UUIDField()
    class Meta:
        unique_together = ("user_id", "entretien_id")

class UserEntreprise(models.Model):
    user_id = models.UUIDField()
    entreprise_id = models.UUIDField()
    class Meta:
        unique_together = ("user_id", "entreprise_id")

class UserContact(models.Model):
    user_id = models.UUIDField()
    contact_id = models.UUIDField()
    class Meta:
        unique_together = ("user_id", "contact_id")

class UserRelance(models.Model):
    user_id = models.UUIDField()
    relance_id = models.UUIDField()
    class Meta:
        unique_together = ("user_id", "relance_id")

class UserEvent(models.Model):
    user_id = models.UUIDField()
    event_id = models.UUIDField()
    class Meta:
        unique_together = ("user_id", "event_id")

class UserProfile(models.Model):
    user_id = models.UUIDField()
    profile_id = models.UUIDField()
    class Meta:
        unique_together = ("user_id", "profile_id")


class RelanceAppel(models.Model):
    relance_id = models.UUIDField()
    appel_id = models.UUIDField()
    class Meta:
        unique_together = ("relance_id", "appel_id")
        
