from apps.common.viewsets import BaseViewSet
from .models import UserProfile
from .serializers import UserProfileSerializer
from logic.profile_service import ProfileService

class UserProfileViewSet(BaseViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
