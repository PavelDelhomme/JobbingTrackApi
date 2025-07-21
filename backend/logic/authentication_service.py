# backend/logic/authentication_service.py
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

class AuthenticationService:
    @staticmethod
    def revoke_all_tokens(user):
        OutstandingToken.objects.filter(user=user).delete()
    
    @staticmethod
    def request_password_reset(user, email):
        """Génère token de reset et envoie email"""
        from apps.authentification.models import PasswordResetToken
        
        # Supprime les anciens tokens
        PasswordResetToken.objects.filter(user=user).delete()
        
        # Crée nouveau token
        token = str(uuid.uuid4())
        expires_at = datetime.now() + timedelta(hours=24)
        
        PasswordResetToken.objects.create(
            user=user,
            token=token,
            expires_at=expires_at
        )
        
        # Envoie email
        reset_url = f"{settings.FRONTEND_URL}/reset-password/?token={token}"
        send_mail(
            subject="Réinitialisation de votre mot de passe",
            message=f"Cliquez sur ce lien pour réinitialiser votre mot de passe : {reset_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        
        return token
    
    @staticmethod
    def confirm_password_reset(token, new_password):
        """Vérifie token et change mot de passe"""
        from apps.authentification.models import PasswordResetToken
        
        try:
            reset_token = PasswordResetToken.objects.get(
                token=token,
                expires_at__gt=datetime.now()
            )
            user = reset_token.user
            user.set_password(new_password)
            user.save()
            
            # Révoque tous les JWT
            AuthenticationService.revoke_all_tokens(user)
            
            # Supprime le token utilisé
            reset_token.delete()
            
            return True
        except PasswordResetToken.DoesNotExist:
            return False
