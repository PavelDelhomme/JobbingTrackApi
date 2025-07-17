from apps.common.serializers import BaseModelSerializer
from .models import Application

class ApplicationSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Application
        fields = '__all__'
