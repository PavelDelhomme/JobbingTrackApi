from apps.common.serializers import BaseModelSerializer
from .models import Company
from apps.common.serializers_registry import register

@register(Company)
class CompanySerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Company
        fields = '__all__'