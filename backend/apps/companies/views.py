from apps.common.utils.factory import crud_viewset
from .models import Company
from .serializers import CompanySerializer
from logic.company_service import CompanyService

class _CompanyViewSet(crud_viewset(Company, CompanySerializer)):
    def perform_create(self, serializer):
        company = serializer.save(user=self.request.user)
        CompanyService.suggest_type(company)

    def perform_update(self, serializer):
        company = serializer.save()
        CompanyService.suggest_type(company)

CompanyViewSet = _CompanyViewSet
