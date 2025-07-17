from apps.common.serializers import BaseModelSerializer
from .models import Calendar

class CalendarSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Calendar
        fields = '__all__'
