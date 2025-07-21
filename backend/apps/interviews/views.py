from apps.common.viewsets import BaseViewSet
from .models import Interview
from .serializers import InterviewSerializer
from logic.interview_service import InterviewService

class InterviewViewSet(BaseViewSet):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer

    def perform_create(self, serializer):
        itw = serializer.save(user=self.request.user)
        InterviewService.on_create(itw)

    def perform_update(self, serializer):
        old = self.get_object()
        itw = serializer.save()
        InterviewService.on_update(itw, old.interview_ts)
