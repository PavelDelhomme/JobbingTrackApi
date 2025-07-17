from rest_framework import generics
from .models import Cv
from apps.common.viewsets import BaseViewSet
from .serializers import CvSerializer
from rest_framework.permissions import IsAuthenticated
from .services import CvService

class CVViewSet(BaseViewSet):
    queryset = CV.objects.all()
    serializer_class = CvSerializer

class CvListView(generics.ListCreateAPIView):
    serializer_class = CvSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cv.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CvDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CvSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cv.objects.filter(user=self.request.user)
