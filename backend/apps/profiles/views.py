from apps.common.viewsets import BaseViewSet
from .models import UserProfile
from .serializers import UserProfileSerializer
from logic.profile_service import ProfileService
from rest_framework.decorators import action
from rest_framework.response import Response

class UserProfileViewSet(BaseViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        profile = request.user.userprofile
        ProfileService.refresh_stats(profile)
        return Response(ProfileService.get_dashboard(profile))
