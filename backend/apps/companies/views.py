"""
from apps.common.utils.factory import crud_viewset
from .models import Company
from .serializers import CompanySerializer
from logic.company_service import CompanyService
from rest_framework.filters import SearchFilter
from apps.common.viewsets import BaseViewSet

class _CompanyVS(crud_viewset(Company, CompanySerializer)):
    filter_backends = BaseViewSet.filter_backends + [SearchFilter]
    search_fields = BaseViewSet.search_fields + ['name', 'sector']
    
    def perform_create(self, serializer):
        company = serializer.save(user=self.request.user)
        CompanyService.suggest_type(company)
        CompanyService.on_create(company)

    def perform_update(self, serializer):
        company = serializer.save()
        CompanyService.suggest_type(company)

CompanyViewSet = _CompanyVS
"""
from apps.common.utils.factory import crud_viewset
from rest_framework.filters import SearchFilter
from .models import Company
from .serializers import CompanySerializer
from logic.company_service import CompanyService

CompanyViewSet = crud_viewset(
    Company,
    CompanySerializer,
    on_create=lambda c: (CompanyService.suggest_type(c), CompanyService.on_create(c)),
    on_update=CompanyService.suggest_type,
    extra_backends=[SearchFilter],
    search_fields=['name', 'sector']
)
