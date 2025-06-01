from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import EvenementViewSet

router = DefaultRouter()
router.register(r'', EvenementViewSet, basename='evenement')

urlpatterns = router.urls
