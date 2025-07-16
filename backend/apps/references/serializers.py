from apps.common.serializers import BaseModelSerializer
from .models import Reference

class ReferenceSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Reference
        fields = '__all__'
