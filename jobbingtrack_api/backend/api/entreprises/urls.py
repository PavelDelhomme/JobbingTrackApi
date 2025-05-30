from django.urls import path
from . import views

urlpatterns = [
    path('entreprises/', views.EntrepriseList.as_view()),
    path('entreprises/<int:pk>/', views.EntrepriseDetail.as_view()),
]