from django.dispatch import receiver
from django.db.models.signals import post_save

from backend.apps.profiles.models import UserProfile, UserSettings


@receiver(post_save, sender=UserProfile)
def auto_settings(sender, instance, created, **kwargs):
    if created:
        UserSettings.objects.create(profile=instance)