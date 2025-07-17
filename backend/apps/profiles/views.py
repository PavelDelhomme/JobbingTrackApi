from apps.common.viewsets import BaseViewSet
from .models import UserProfile
from .serializers import UserProfileSerializer

class UserProfileViewSet(BaseViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
