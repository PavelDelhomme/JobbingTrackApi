from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, MeView
from .views import RequestPasswordResetView, ConfirmPasswordResetView

urlpatterns = [
    path('register/', RegisterView.as_view(),          name='register'),
    path('login/',    TokenObtainPairView.as_view(),   name='token_obtain_pair'),
    path('refresh/',  TokenRefreshView.as_view(),      name='token_refresh'),
    path('me/',       MeView.as_view(),                name='me'),
    path('reset/',    RequestPasswordResetView.as_view(), name='request-password-reset'),
    path('reset/<uid>/<token>', ConfirmPasswordResetView.as_view(), name='confirm-password-reset'),
]
