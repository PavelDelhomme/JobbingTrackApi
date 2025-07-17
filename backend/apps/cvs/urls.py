from django.urls import path
from .views import CvListView, CvDetailView

urlpatterns = [
    path('', CvListView.as_view()),
    path('<uuid:pk>/', CvDetailView.as_view()),
]
