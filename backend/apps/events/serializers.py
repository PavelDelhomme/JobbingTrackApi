from apps.common.serializers import BaseModelSerializer
from .models import Event

class EventSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Event
        fields = '__all__'
