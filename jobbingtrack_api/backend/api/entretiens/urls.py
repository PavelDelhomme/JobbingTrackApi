from django.urls import path
from . import views

urlpatterns = [
    path('entretiens/', views.EntretienList.as_view()),
    path('entretiens/<int:pk>/', views.EntretienDetail.as_view()),
]