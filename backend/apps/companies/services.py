import uuid
import time

class CompanyService:
    @staticmethod
    def create_minimal_company(name, user):
        """
        Créée une entreprise minimal avec juste un nom
        """
        from .models import Company

        # Créer une entreprise minimale
        timestamp = int(time.time() * 1000)
        company = Company.objects.create(
            id=str(uuid.uuid4()),
            name=name,
            user=user,
            created_at=timestamp,
            updated_at=timestamp,
            is_archived=False,
            is_deleted=False,
        )

        return company