from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CandidatureViewSet

router = DefaultRouter()
router.register(r'', CandidatureViewSet, basename='candidatures')

urlpatterns = router.urls
