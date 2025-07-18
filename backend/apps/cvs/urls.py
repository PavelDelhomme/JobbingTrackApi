from rest_framework_nested import routers
from .views import (
    CvViewSet, EducationViewSet, ExperienceViewSet,
    SkillViewSet, LanguageViewSet, ProjectViewSet, CertificationViewSet
)

router = routers.DefaultRouter()
router.register(r'cvs', CvViewSet, basename='cvs')

cvs_router = routers.NestedDefaultRouter(router, r'cvs', lookup='cv')
cvs_router.register(r'educations', EducationViewSet, basename='cv-educations')
cvs_router.register(r'experiences', ExperienceViewSet, basename='cv-experiences')
cvs_router.register(r'skills', SkillViewSet, basename='cv-skills')
cvs_router.register(r'languages', LanguageViewSet, basename='cv-languages')
cvs_router.register(r'projects', ProjectViewSet, basename='cv-projects')
cvs_router.register(r'certifications', CertificationViewSet, basename='cv-certifications')

urlpatterns = router.urls + cvs_router.urls