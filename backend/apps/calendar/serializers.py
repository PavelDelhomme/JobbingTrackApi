from apps.common.serializers import BaseModelSerializer
from .models import Calendar
from apps.common.serializers_registry import register

@register(Calendar)
class CalendarSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Calendar
        fields = '__all__'
