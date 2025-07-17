from rest_framework.routers import DefaultRouter
from .views import FollowUpViewSet

router = DefaultRouter()
router.register(r'', FollowUpViewSet, basename='followups')

urlpatterns = router.urls