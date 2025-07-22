from django.conf import settings
from django.core.mail import send_mail
import uuid
import time
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    @staticmethod
    def send_email_notification(user, subject, message):
        """
        Envoie une notification par email
        """
        # Vérifier les préférences de l'utilisateur
        try:
            from apps.profiles.models import UserProfile
            profile = UserProfile.objects.get(user=user)
            
            if not profile.email_notifications:
                return False
                
        except UserProfile.DoesNotExist:
            # Par défaut, on envoie l'email
            pass
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False
            )
            return True
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi de l'email: {str(e)}")
            return False
    
    @staticmethod
    def create_push_notification(user, title, body, data=None):
        """
        Crée une notification push dans la base de données
        """
        from apps.common.models.notification import PushNotification
        
        # Vérifier les préférences de l'utilisateur
        try:
            from apps.profiles.models import UserProfile
            profile = UserProfile.objects.get(user=user)
            
            if not profile.push_notifications:
                return None
                
        except UserProfile.DoesNotExist:
            # Par défaut, on envoie la notification
            pass
        
        timestamp = int(time.time() * 1000)
        notification = PushNotification.objects.create(
            id=str(uuid.uuid4()),
            user=user,
            title=title,
            body=body,
            data=data or {},
            created_at=timestamp,
            is_read=False
        )
        
        # TODO: Envoyer la notification push via Firebase ou autre service
        
        return notification
    
    @staticmethod
    def notify_upcoming_interview(interview):
        """
        Envoie une notification pour un entretien à venir
        """
        from datetime import datetime, timedelta
        
        # Convertir le timestamp en datetime
        interview_dt = datetime.fromtimestamp(interview.interview_ts / 1000)
        now = datetime.now()
        
        # Calculer le délai
        delta = interview_dt - now
        
        # Entretien dans moins de 24h
        if delta < timedelta(hours=24) and delta > timedelta(hours=0):
            subject = f"Rappel: Entretien avec {interview.company_name} demain"
            message = f"""
            Bonjour,
            
            Nous vous rappelons que vous avez un entretien demain avec {interview.company_name}.
            
            Date: {interview_dt.strftime('%d/%m/%Y à %H:%M')}
            Lieu: {interview.location or 'Non spécifié'}
            
            Bon courage!
            L'équipe JobbingTrack
            """
            
            NotificationService.send_email_notification(
                interview.user,
                subject,
                message
            )
            
            NotificationService.create_push_notification(
                interview.user,
                "Rappel d'entretien",
                f"Entretien avec {interview.company_name} demain à {interview_dt.strftime('%H:%M')}",
                {
                    "type": "interview",
                    "id": str(interview.id)
                }
            )
    
    @staticmethod
    def notify_pending_followup(followup):
        """
        Envoie une notification pour une relance en attente
        """
        subject = f"Relance à effectuer: {followup.title}"
        message = f"""
        Bonjour,
        
        Nous vous rappelons que vous avez une relance à effectuer pour {followup.company_name}.
        
        Titre: {followup.title}
        Description: {followup.description}
        
        Cordialement,
        L'équipe JobbingTrack
        """
        
        NotificationService.send_email_notification(
            followup.user,
            subject,
            message
        )
        
        NotificationService.create_push_notification(
            followup.user,
            "Relance à effectuer",
            f"N'oubliez pas de relancer {followup.company_name}",
            {
                "type": "followup",
                "id": str(followup.id)
            }
        )