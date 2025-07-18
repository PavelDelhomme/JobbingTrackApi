from rest_framework.decorators import action
from rest_framework.response import Response
from apps.common.viewsets import BaseViewSet
from .models import UserProfile
from .serializers import UserProfileSerializer
from logic.profile_service import ProfileService

class UserProfileViewSet(BaseViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    
    def retrieve(self, request, *args, **kwargs):
        # Expose aussi les stats dans la réponse "me/profile"
        instance = self.get_object()
        data = self.get_serializer(instance).data
        data['stats_7d'] = ProfileService.stats_last_7_days(request.user)
        return Response(data)

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Retourne les stats + paramètres dashboard."""
        profile = UserProfile.objects.get(user=request.user)
        ProfileService.refresh_stats(profile)
        return Response(ProfileService.get_dashboard(profile))