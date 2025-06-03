from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .views import (
    RegisterView, LoginView, MeView, LogoutView, ActiveTokensView, LogoutAllView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout_all_tokens'),
    path('logout-all/', LogoutAllView.as_view(), name='logout_all'),
    path('me/', MeView.as_view(), name='me'),
    path('tokens/', ActiveTokensView.as_view(), name='active_tokens'),  # optionnel
]
