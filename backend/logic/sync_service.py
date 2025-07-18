# backend/logic/sync_service.py
from django.apps import apps

class SyncService:
    @staticmethod
    def changed_since(model_label, user, ts):
        model = apps.get_model(model_label)
        return model.objects.filter(
            user=user,
            updated_at__gt=ts,
            is_deleted=False
        )
