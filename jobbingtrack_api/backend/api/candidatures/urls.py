from django.urls import path
from . import views

urlpatterns = [
    path('candidatures/', views.CandidatureList.as_view()),
    path('candidatures/<int:pk>/', views.CandidatureDetail.as_view()),
]