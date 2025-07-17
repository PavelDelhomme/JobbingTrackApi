from apps.common.serializers import BaseModelSerializer
from .models import Call

class CallSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Call
        fields = '__all__'