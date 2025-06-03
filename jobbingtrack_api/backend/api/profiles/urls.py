from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, CVViewSet, LanguageViewSet, ExperienceViewSet, EducationViewSet, ProjectViewSet, UploadCVView

router = DefaultRouter()
router.register(r'profiles/', ProfileViewSet)
router.register(r'cvs', CVViewSet)
router.register(r'languages', LanguageViewSet)
router.register(r'experiences', ExperienceViewSet)
router.register(r'educations', EducationViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'upload', UploadCVView)

urlpatterns = router.urls

#urlpatterns = router.urls + [
#    path("upload-cv/", UploadCVView.as_view(), name="upload_cv"),
#]
urlpatterns += [path('upload-cv/', UploadCVView.as_view(), name='upload-cv')]