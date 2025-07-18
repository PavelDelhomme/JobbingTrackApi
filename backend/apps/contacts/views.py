from apps.common.viewsets import BaseViewSet
from .models import Contact
from .serializers import ContactSerializer
from backend.apps.common.utils.factory import viewset_factory

#class ContactViewSet(BaseViewSet):
#    queryset = Contact.objects.all()
#    serializer_class = ContactSerializer

ContactViewSet = viewset_factory(Contact, ContactSerializer)