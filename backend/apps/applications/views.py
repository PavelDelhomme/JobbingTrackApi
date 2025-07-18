from apps.common.viewsets import BaseViewSet
from .models import Application
from .serializers import ApplicationSerializer
from logic.application_service import ApplicationService

class ApplicationViewSet(BaseViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def perform_create(self, serializer):
        app = serializer.save(user=self.request.user)
        ApplicationService.on_create(app)

    def perform_update(self, serializer):
        old = self.get_object()
        app = serializer.save()
        ApplicationService.on_update(app, old.application_ts)