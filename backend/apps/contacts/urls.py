from rest_framework.routers import DefaultRouter
from .views import ContactViewSet

router = DefaultRouter()
router.register(r'', ContactViewSet, basename='contacts')

urlpatterns = router.urls