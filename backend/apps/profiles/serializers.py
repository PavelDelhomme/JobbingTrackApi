from apps.common.serializers import BaseModelSerializer
from .models import UserProfile
from apps.common.serializers_registry import register

@register(UserProfile)
class UserProfileSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = UserProfile
        fields = '__all__'
