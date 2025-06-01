from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AppelViewSet, AppelList, AppelDetail

router = DefaultRouter()
router.register(r'', AppelViewSet, basename='appels')

urlpatterns = [
    path('appels/list/', AppelList.as_view()),
    path('appels/detail/<uuid:pk>/', AppelDetail.as_view()),
]

urlpatterns += router.urls
