from rest_framework.routers import DefaultRouter
from .views import ReferenceViewSet

router = DefaultRouter()
router.register(r'', ReferenceViewSet, basename='references')

urlpatterns = router.urls
