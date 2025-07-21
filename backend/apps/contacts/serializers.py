from apps.common.serializers import BaseModelSerializer
from .models import Contact
from apps.common.serializers_registry import register

@register(Contact)
class ContactSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Contact
        fields = '__all__'