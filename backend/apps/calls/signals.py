from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Call

@receiver(post_save, sender=Call)
def call_post_save(sender, instance, created, **kwargs):
    """
    Actions à effectuer après la sauvegarde d'un appel
    """
    if created:
        # Création d'un événement
        from apps.events.services import EventService
        EventService.create_call_event(instance)

        # Mise à jour du profil utilisateur
        from apps.profiles.services import ProfileService
        ProfileService.update_stats(instance.user)