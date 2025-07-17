from apps.common.viewsets import BaseViewSet
from .models import Contact
from .serializers import ContactSerializer

class ContactViewSet(BaseViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
