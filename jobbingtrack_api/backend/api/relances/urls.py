from django.urls import path
from . import views

urlpatterns = [
    path('relances/', views.RelanceList.as_view()),
    path('relances/<int:pk>/', views.RelanceDetail.as_view()),
]