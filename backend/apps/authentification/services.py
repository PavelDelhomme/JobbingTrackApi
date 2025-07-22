import uuid
import secrets
import datetime
from django.utils import timezone
from django.db import transaction

class AuthenticationService:
    @staticmethod
    def create_user(email, password, first_name="", last_name=""):
        """
        Crée un nouvel utilisateur et son profil
        """
        from apps.authentification.models import User, UserPermissions
        from apps.profiles.services import ProfileService
        
        with transaction.atomic():
            # Créer l'utilisateur
            user = User.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            # Créer les permissions
            UserPermissions.objects.create(
                user=user,
                role='CLIENT'
            )
            
            # Créer le profil
            ProfileService.create_empty_profile(user)
        
        return user
    
    @staticmethod
    def request_password_reset(user, email):
        """
        Génère un token pour la réinitialisation de mot de passe
        """
        from apps.authentification.models import PasswordResetToken
        
        # Supprimer les anciens tokens
        PasswordResetToken.objects.filter(user=user).delete()
        
        # Générer un nouveau token
        token = secrets.token_urlsafe(32)
        expires_at = timezone.now() + datetime.timedelta(hours=24)
        
        # Enregistrer le token
        reset_token = PasswordResetToken.objects.create(
            user=user,
            token=token,
            expires_at=expires_at
        )
        
        # TODO: Envoyer l'email avec le lien de réinitialisation
        # from django.core.mail import send_mail
        # send_mail(
        #     'Réinitialisation de votre mot de passe',
        #     f'Cliquez sur ce lien pour réinitialiser votre mot de passe: http://votre-site.com/reset/{token}',
        #     'noreply@votre-site.com',
        #     [email],
        #     fail_silently=False,
        # )
        
        return reset_token
    
    @staticmethod
    def confirm_password_reset(token, new_password):
        """
        Vérifie le token et change le mot de passe
        """
        from apps.authentification.models import PasswordResetToken
        
        try:
            # Récupérer le token
            reset_token = PasswordResetToken.objects.get(token=token)
            
            # Vérifier qu'il n'est pas expiré
            if reset_token.expires_at < timezone.now():
                return False
            
            # Changer le mot de passe
            user = reset_token.user
            user.set_password(new_password)
            user.save()
            
            # Supprimer le token
            reset_token.delete()
            
            return True
        except PasswordResetToken.DoesNotExist:
            return False