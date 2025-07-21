from apps.common.serializers import BaseModelSerializer
from .models import Call
from apps.common.serializers_registry import register

@register(Call)
class CallSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Call
        fields = '__all__'