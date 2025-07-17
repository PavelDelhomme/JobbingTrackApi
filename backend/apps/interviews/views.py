from apps.common.viewsets import BaseViewSet
from .models import Interview
from .serializers import InterviewSerializer

class InterviewViewSet(BaseViewSet):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer

    def get_queryset(self):
        """Filtre par utilisateur et exclut les éléments supprimés"""
        return self.queryset.filter(
            user=self.request.user,
            is_deleted=False
        )