from relances.models import Relance
from candidatures.models import Candidature
from entreprises.models import Entreprise
from django.utils import timezone

def create_relance(user_id, candidature_id, message="", status="En attente"):
    try:
        candidature = Candidature.objects.get(id=candidature_id)
    except Candidature.DoesNotExist:
        raise ValueError("Candidature inexistante")

    entreprise_id = candidature.company_id

    relance = Relance.objects.create(
        user_id=user_id,
        candidature_id=candidature_id,
        entreprise_id=entreprise_id,
        date=timezone.now(),
        message=message,
        status=status
    )
    return relance
