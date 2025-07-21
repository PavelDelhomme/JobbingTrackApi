from apps.common.serializers import BaseModelSerializer
from .models import FollowUp
from apps.common.serializers_registry import register

@register(FollowUp)
class FollowUpSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = FollowUp
        fields = '__all__'
        