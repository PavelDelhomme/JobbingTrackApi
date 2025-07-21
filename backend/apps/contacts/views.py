from apps.common.viewsets import BaseViewSet
from .models import Contact
from .serializers import ContactSerializer
from logic.contact_service import ContactService

class ContactViewSet(BaseViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def perform_create(self, serializer):
        contact = serializer.save(user=self.request.user)
        ContactService.attach_company(contact)

    def perform_update(self, serializer):
        contact = serializer.save()
        ContactService.attach_company(contact)
