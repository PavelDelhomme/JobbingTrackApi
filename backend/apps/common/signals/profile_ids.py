from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps
from apps.profiles.models import UserProfile


TRACKED_MODELS = [
    'applications.Application',
    'companies.Company',
    'contacts.Contact',
    'calls.Call',
    'followups.FollowUp',
    'interviews.Interview',
    'events.Event',
]

@receiver(post_save)
def add_id_to_profile(sender, instance, created, **kw):
    label = f'{sender._meta.app_label}.{sender.__name__}'
    if not created or label not in TRACKED_MODELS:
        return
    profile = instance.user.userprofile
    field = f"{sender._meta.model_name}_ids"   # ex : application_ids
    ids = getattr(profile, field, None)
    if ids is not None and instance.id not in ids:
        ids.append(instance.id)
        setattr(profile, field, ids)
        profile.save(update_fields=[field])