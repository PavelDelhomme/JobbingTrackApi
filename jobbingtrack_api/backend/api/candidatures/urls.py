from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CandidatureViewSet

router = DefaultRouter()
router.register(r'candidatures', CandidatureViewSet, basename='candidatures')

urlpatterns = router.urls
