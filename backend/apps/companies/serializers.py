from apps.common.serializers import BaseModelSerializer
from .models import Company

class CompanySerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Company
        fields = '__all__'