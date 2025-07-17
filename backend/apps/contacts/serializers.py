from apps.common.serializers import BaseModelSerializer
from .models import Contact

class ContactSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Contact
        fields = '__all__'