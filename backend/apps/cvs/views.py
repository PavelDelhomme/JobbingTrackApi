from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from apps.common.permissions import IsOwnerOrReadOnly
from apps.common.filters import UpdatedAfterFilter
from .models import (Cv, Education, Experience, Skill, Language, Project, Certification)
from .serializers import (CvSerializer, EducationSerializer, ExperienceSerializer,
                         SkillSerializer, LanguageSerializer, ProjectSerializer, 
                         CertificationSerializer)
from logic.cv_service import CvService

class CvViewSet(viewsets.ModelViewSet):
    queryset = Cv.objects.all()
    serializer_class = CvSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [UpdatedAfterFilter]

    def perform_create(self, serializer):
        cv = serializer.save(user=self.request.user)
        CvService.on_create(cv)

    def perform_update(self, serializer):
        cv = serializer.save()
        CvService.on_update(cv)

class _Child(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [UpdatedAfterFilter]
    
    def get_queryset(self):
        return self.model.objects.filter(
            cv_id=self.kwargs["cv_pk"], 
            user=self.request.user,
            is_deleted=False
        ).order_by("-updated_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, cv_id=self.kwargs["cv_pk"])

class EducationViewSet(_Child):
    model = Education
    serializer_class = EducationSerializer

class ExperienceViewSet(_Child):
    model = Experience
    serializer_class = ExperienceSerializer

class SkillViewSet(_Child):
    model = Skill
    serializer_class = SkillSerializer

class LanguageViewSet(_Child):
    model = Language
    serializer_class = LanguageSerializer

class ProjectViewSet(_Child):
    model = Project
    serializer_class = ProjectSerializer

class CertificationViewSet(_Child):
    model = Certification
    serializer_class = CertificationSerializer
