from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    UserSerializer, RegisterSerializer, 
    EmailSerializer, ResetSerializer
)
from .models import User
from .services import AuthenticationService
from rest_framework.exceptions import ValidationError

# Vue fonctionnelle pour l'inscription
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Inscription d'un nouvel utilisateur
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Créer les tokens JWT
        refresh = RefreshToken.for_user(user)
        
        # Créer la réponse
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vue basée sur une classe pour "me"
class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user

# Vue pour demander une réinitialisation
class RequestPasswordResetView(generics.CreateAPIView):
    serializer_class = EmailSerializer
    permission_classes = [permissions.AllowAny]
    
    def perform_create(self, serializer):
        try:
            user = User.objects.get(email=serializer.validated_data['email'])
            AuthenticationService.request_password_reset(
                user, serializer.validated_data['email']
            )
        except User.DoesNotExist:
            # Ne pas révéler si l'email existe ou non (sécurité)
            pass

# Vue pour confirmer la réinitialisation
class ConfirmPasswordResetView(generics.CreateAPIView):
    serializer_class = ResetSerializer
    permission_classes = [permissions.AllowAny]
    
    def perform_create(self, serializer):
        ok = AuthenticationService.confirm_password_reset(
            serializer.validated_data['token'],
            serializer.validated_data['new_password']
        )
        if not ok:
            raise ValidationError("Token invalide ou expiré")