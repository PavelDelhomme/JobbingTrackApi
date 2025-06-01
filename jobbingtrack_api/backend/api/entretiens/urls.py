from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import EntretienViewSet

router = DefaultRouter()
router.register(r'', EntretienViewSet, basename='entretien')

urlpatterns = router.urls
