from django.forms import ValidationError
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegistrationSerializer, UserSerializer, EmailSerializer, ResetSerializer
from .models import User
from logic.authentication_service import AuthenticationService


class RegisterView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]


class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class RequestPasswordResetView(generics.CreateAPIView):
    serializer_class = EmailSerializer
    permission_classes = [permissions.AllowAny]
    
    def perform_create(self, serializer):
        user = User.objects.get(email=serializer.validated_data['email'])
        AuthenticationService.request_password_reset(
            user, serializer.validated_data['email']
        )

class ConfirmPasswordResetView(generics.CreateAPIView):
    serializer_class = ResetSerializer
    permissions_classes = [permissions.AllowAny]
    
    def perform_create(self, serializer):
        ok = AuthenticationService.confirm_password_reset(
            serializer.validated_data['token'],
            serializer.validated_data['new_password']
        )
        if not ok:
            raise ValidationError("Token invalide ou expiré")