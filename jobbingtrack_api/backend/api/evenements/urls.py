from django.urls import path
from . import views

urlpatterns = [
    path('evenements/', views.EvenementList.as_view()),
    path('evenements/<int:pk>/', views.EvenementDetail.as_view()),
]