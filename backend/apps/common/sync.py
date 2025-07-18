from rest_framework.decorators import api_vieww, permission_classes
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sync_endpoint(request):
    since = int(request.query_params.get("updated_after", 0))
    payload = {}
    for key, label in MODELS.items():
        objs = SyncService.changed_since(label, request.user, since)
        payload[key] = list(objs.values()) # Ou Serializer(objs, many=True).data
    return Response(payload)