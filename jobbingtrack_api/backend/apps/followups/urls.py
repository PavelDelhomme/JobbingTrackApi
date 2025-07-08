from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import FollowUpViewSet

router = DefaultRouter()
router.register(r'followups', FollowUpViewSet, basename='followups')

urlpatterns = router.urls
