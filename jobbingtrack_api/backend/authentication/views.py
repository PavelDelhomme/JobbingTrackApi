from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
User = get_user_model()
from rest_framework import generics, permissions

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

from django.db import transaction

from api.profiles.models import Profile

from .serializers import RegisterSerializer, UserSerializer

class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        self.user = serializer.save()
        Profile.objects.create(
            user_id=self.user.id,
            subject="Profil par défaut",
            notes="Créé automatiquement à l’inscription",
            company_ids=[],
            contact_ids=[],
            candidature_ids=[],
            relance_ids=[],
        )
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        refresh = RefreshToken.for_user(self.user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": str(self.user.id),
                "email": self.user.email,
            }
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email et mot de passe requis"}, status=400)

        user = authenticate(request, email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                }
            })
        return Response({"error": "Identifiants invalides"}, status=401)
    
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Déconnexion réussie."}, status=205)
        except Exception as e:
            return Response({"error": "Token invalide ou déjà révoqué."}, status=400)


class LogoutAllView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user=request.user)
        for token in tokens:
            _, _ = BlacklistedToken.objects.get_or_create(token=token)
        return Response({"detail": "Tous les tokens ont été révoqués."}, status=205)

class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class ActiveTokensView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        tokens = OutstandingToken.objects.filter(user=request.user)
        return Response([
            {
                "token": t.token,
                "created": t.created,
                "expires_at": t.expires_at,
                "jti": t.jti
            } for t in tokens if not t.blacklisted
        ])
