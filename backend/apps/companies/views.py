from apps.common.viewsets import BaseViewSet
from .models import Company
from .serializers import CompanySerializer

class CompanyViewSet(BaseViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer