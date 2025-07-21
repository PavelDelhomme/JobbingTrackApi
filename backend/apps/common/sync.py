from apps.common.serializers_registry import get_serializer_for_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from logic.sync_service import SyncService

MODELS = {
    "applications": "applications.Application",
    "companies":    "companies.Company",
    "calls":        "calls.Call",
    "followups":    "followups.FollowUp",
    "interviews":   "interviews.Interview",
    "contacts":     "contacts.Contact",
    "cvs":          "cvs.Cv",
    "events":       "events.Event",
    "profiles":     "profiles.UserProfile",
    "references":   "references.Reference",
    "calendar":     "calendar.Calendar",
    "user_settings": "profiles.UserSettings"    
}

def serialize_instance(instance, request):
    """
    Sérialise un objet à l’aide du ModelSerializer enregistré.
    Le serializer reçoit request dans le contexte pour être cohérent
    avec le reste de l’API (URL absolues éventuelles, etc.)
    """
    serializer_cls = get_serializer_for_model(type(instance))
    if not serializer_cls:
        # Fallback très léger : return __dict__ (sans _state)
        data = vars(instance).copy()
        data.pop('_state', None)
        return data
    return serializer_cls(instance, context={'request': request}).data


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sync_endpoint(request):
    since = int(request.query_params.get("updated_after", 0))
    payload = {}
    
    for key, label in MODELS.items():
        changes = []
        ledger = SyncService.get_ledger(request.user, label)
        last_hash = ledger.last_hash if ledger else None
        
        # Récupère les objets modifiés avec leur hash
        changed_objects = SyncService.changed_since(label, request.user, since)
        
        for obj, new_hash in changed_objects:
            # Envoie seulement si hash différent ou pas de ledger
            if not last_hash or new_hash != last_hash:
                changes.append({
                    "id": str(obj.id),
                    "data": serialize_instance(obj, request), ## Modifie moi cela s'il te plait donc
                    "hash": new_hash
                })
        
        payload[key] = changes
        
        # Met à jour le ledger avec le dernier hash si nécessaire
        if changed_objects:
            SyncService.update_ledger(
                request.user,
                label,
                changed_objects[-1][1] # Dernier hash
            )
            
    return Response(payload)