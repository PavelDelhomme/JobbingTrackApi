from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Interview

@receiver(post_save, sender=Interview)
def interview_post_save(sender, instance, created, **kwargs):
    """
    Actions à effectuer après la sauvegarde d'un entretien
    """
    if created:
        # Création d'un événement
        from apps.events.services import EventService
        EventService.create_interview_event(instance)

        # Mise à jour du profil utilisateur
        from apps.profiles.services import ProfileService
        ProfileService.update_stats(instance.user)