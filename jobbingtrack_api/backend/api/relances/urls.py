from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RelanceViewSet

router = DefaultRouter()
router.register(r'relances', RelanceViewSet, basename='relance')

urlpatterns = router.urls
