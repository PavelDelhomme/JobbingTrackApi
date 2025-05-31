from .base import BaseModel
from .linking_models import (
    # CANDIDATURES RELATIONS
    CandidatureContact,
    CandidatureRelance,
    CandidatureAppel,
    CandidatureEntretien,
    CandidatureEntreprise,

    # CONTACTS RELATIONS
    ContactEntreprise,
    ContactAppel,
    ContactEntretien,
    ContactRelance,

    # ENTREPRISE RELATIONS
    EntrepriseAppel,
    EntrepriseRelance,
    EntrepriseEntretien,

    # EVENTS RELATIONS
    CandidatureEvent,
    RelanceEvent,
    EntretienEvent,
    EntrepriseEvent,

    # USER RELATIONS
    UserCandidature,
    UserAppel,
    UserEntretien,
    UserEntreprise,
    UserContact,
    UserRelance,
    UserEvent,
    UserProfile,

    # AUTRES RELATIONS
    RelanceAppel,
    AppelEvent,
)
