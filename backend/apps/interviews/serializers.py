from apps.common.serializers import BaseModelSerializer
from .models import Interview
from apps.common.serializers_registry import register

@register(Interview)
class InterviewSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Interview
        fields = '__all__'
