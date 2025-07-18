from apps.common.viewsets import BaseViewSet
from rest_framework import mixins
from .models import (
    Cv, Education, Experience, Skill,
    Language, Project, Certification
)
from .serializers import (
    CvSerializer, EducationSerializer, ExperienceSerializer,
    SkillSerializer, LanguageSerializer, ProjectSerializer,
    CertificationSerializer
)
from logic.cv_service import CvService


class CvViewSet(BaseViewSet):
    queryset = Cv.objects.all()
    serializer_class = CvSerializer
    
    def perform_create(self, serializer):
        cv = serializer.save(user=self.request.user)
        CvService.ensure_single_primary(cv)
    
    def perform_update(self, serializer):
        cv = serializer.save()
        CvService.ensure_single_primary(cv)


class _Child(BaseViewSet,
             mixins.CreateModelMixin,
             mixins.UpdateModelMixin,
             mixins.DestroyModelMixin,
             mixins.ListModelMixin,
             mixins.RetrieveModelMixin):
    """Vue de base partagée par toutes les sous-ressources CV."""
    def get_queryset(self):
        return self.model.objects.filter(cv_id=self.kwargs["cv_pk"], user=self.request.user, is_deleted=False)

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

