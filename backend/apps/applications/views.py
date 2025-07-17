from apps.common.viewsets import BaseViewSet
from .models import Application
from .serializers import ApplicationSerializer

class ApplicationViewSet(BaseViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer