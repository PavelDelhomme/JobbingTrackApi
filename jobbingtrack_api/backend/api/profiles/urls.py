from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    ProfileViewSet,
    CVViewSet,
    LanguageViewSet,
    ExperienceViewSet,
    EducationViewSet,
    ProjectViewSet,
    UploadCVView,
)

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'cvs', CVViewSet, basename='cv')
router.register(r'languages', LanguageViewSet, basename='language')
router.register(r'experiences', ExperienceViewSet, basename='experience')
router.register(r'educations', EducationViewSet, basename='education')
router.register(r'projects', ProjectViewSet, basename='project')

# ⛔ NE PAS mettre UploadCVView ici
# router.register(r'upload', UploadCVView)

urlpatterns = router.urls + [
    path('upload-cv/', UploadCVView.as_view(), name='upload-cv'),
]
