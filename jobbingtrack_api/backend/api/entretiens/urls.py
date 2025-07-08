#backend/api/entretiens/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import EntretienViewSet

router = DefaultRouter()
router.register(r'entretiens', EntretienViewSet, basename='entretien')

urlpatterns = router.urls
