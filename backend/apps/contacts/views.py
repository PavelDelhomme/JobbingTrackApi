from apps.common.utils.factory import crud_viewset
from rest_framework.filters import SearchFilter
from .models import Contact
from .serializers import ContactSerializer
from logic.contact_service import ContactService

ContactViewSet = crud_viewset(
    Contact,
    ContactSerializer,
    on_create=ContactService.attach_company,
    on_update=ContactService.attach_company,
    extra_backends=[SearchFilter],
    search_fields=['first_name', 'last_name', 'email', 'company_name', 'phone']
)

"""
class ContactViewSet(BaseViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def perform_create(self, serializer):
        contact = serializer.save(user=self.request.user)
        ContactService.attach_company(contact)

    def perform_update(self, serializer):
        contact = serializer.save()
        ContactService.attach_company(contact)
"""
"""
class _ContactVS(crud_viewset(Contact, ContactSerializer)):
    filter_backends = BaseViewSet.filter_backends + [SearchFilter]
    search_fields = ['first_name', 'last_name', 'email', 'company_name', 'phone']
"""
