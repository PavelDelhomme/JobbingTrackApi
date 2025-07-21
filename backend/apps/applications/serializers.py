from apps.common.serializers_registry import register
from apps.common.serializers import BaseModelSerializer
from .models import Application

@register(Application)
class ApplicationSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Application
        fields = '__all__'
