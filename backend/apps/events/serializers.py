from apps.common.serializers import BaseModelSerializer
from .models import Event
from apps.common.serializers_registry import register


@register(Event)
class EventSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Event
        fields = '__all__'
