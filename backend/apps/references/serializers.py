from apps.common.serializers import BaseModelSerializer
from .models import Reference
from apps.common.serializers_registry import register

@register(Reference)
class ReferenceSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Reference
        fields = '__all__'
