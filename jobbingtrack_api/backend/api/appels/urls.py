from django.urls import path
from . import views

urlpatterns = [
    path('appels/', views.AppelList.as_view()),
    path('appels/<int:pk>/', views.AppelDetail.as_view()),
]