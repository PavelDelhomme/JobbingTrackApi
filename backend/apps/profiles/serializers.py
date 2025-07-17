from apps.common.serializers import BaseModelSerializer
from .models import UserProfile

class UserProfileSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = UserProfile
        fields = '__all__'
