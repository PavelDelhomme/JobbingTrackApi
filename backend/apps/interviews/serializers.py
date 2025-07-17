from apps.common.serializers import BaseModelSerializer
from .models import Interview

class InterviewSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Interview
        fields = '__all__'
