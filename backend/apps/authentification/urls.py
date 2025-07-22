# apps/authentification/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    register_user, MeView, 
    RequestPasswordResetView, ConfirmPasswordResetView
)

urlpatterns = [
    # Vous pouvez choisir entre la vue basée sur une fonction ou une classe
    path('register/', register_user, name='register'),
    # Ou utilisez la vue basée sur une classe si vous préférez
    # path('register/', RegisterView.as_view(), name='register'),
    
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', MeView.as_view(), name='me'),
    path('reset/', RequestPasswordResetView.as_view(), name='request-password-reset'),
    path('reset/confirm/', ConfirmPasswordResetView.as_view(), name='confirm-password-reset'),
]