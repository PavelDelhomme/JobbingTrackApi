from rest_framework import generics
from .models import Cv
from .serializers import CvSerializer
from .services import CvService

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
