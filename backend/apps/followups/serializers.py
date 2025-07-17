from apps.common.serializers import BaseModelSerializer
from .models import FollowUp

class FollowUpSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = FollowUp
        fields = '__all__'
        