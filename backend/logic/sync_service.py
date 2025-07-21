import hashlib
from django.apps import apps
from apps.common.models.sync import SyncLedger
from django.db.models import Q

class SyncService:
    @staticmethod
    def generate_hash(obj):
        """Génère un hash basé sur l'ID et updated_at"""
        data = f"{obj.id}{obj.updated_at.timestamp()}"
        return hashlib.md5(data.encode()).hexdigest()

    @staticmethod
    def get_ledger(user, model_label):
        try:
            return SyncLedger.objects.get(user=user, model_name=model_label)
        except SyncLedger.DoesNotExist:
            return None

    @staticmethod
    def changed_since(model_label, user, ts):
        """Retourne les objets modifiés avec leur hash"""
        model = apps.get_model(model_label)
        return [
            (obj, SyncService.generate_hash(obj))
            for obj in model.objects.filter(
                user=user,
                updated_at__gt=ts,
                is_deleted=False
            )
        ]

    @staticmethod
    def update_ledger(user, model_label, new_hash):
        ledger, _ = SyncLedger.objects.update_or_create(
            user=user,
            model_name=model_label,
            defaults={'last_hash': new_hash}
        )
