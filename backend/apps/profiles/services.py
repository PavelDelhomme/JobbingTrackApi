import time
from datetime import datetime, timedelta

class ProfileService:
    @staticmethod
    def update_stats(user):
        """
        Met à jour les statistiques du profil d'un utilisateur
        """
        from apps.profiles.models import UserProfile

        # Récupérer le profil
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            # Si le profil n'existe pas, le créer
            profile = ProfileService.create_empty_profile(user)
        
        # Calculer la date d'il y a 7 jours en millisecondes
        seven_days_ago = int((datetime.now() - timedelta(days=7)).timestamp() * 1000)

        # Calculer les statistiques
        from apps.applications.models import Application
        from apps.calls.models import Call
        from apps.followups.models import FollowUp
        from apps.interviews.models import Interview
        from apps.contacts.models import Contact

        profile.apps_last_7 = Application.objects.filter(
            user=user,
            created_at__gte=seven_days_ago,
            is_deleted=False
        ).count()


        profile.calls_last_7 = Call.objects.filter(
            user=user,
            created_at__gt=seven_days_ago,
            is_deleted=False
        ).count()
        
        profile.fu_last_7 = FollowUp.objects.filter(
            user=user,
            created_at__gt=seven_days_ago,
            is_deleted=False
        ).count()
        
        profile.itw_last_7 = Interview.objects.filter(
            user=user,
            created_at__gt=seven_days_ago,
            is_deleted=False
        ).count()
        
        profile.contacts_last_7 = Contact.objects.filter(
            user=user,
            created_at__gt=seven_days_ago,
            is_deleted=False
        ).count()
        
        profile.save()
        return profile

    @staticmethod
    def create_empty_profile(user):
        """
        Crée un profil vide pour un utilisateur
        """
        from apps.profiles.models import UserProfile
        
        timestamp = int(time.time() * 1000)
        profile = UserProfile.objects.create(
            id=str(uuid.uuid4()),
            user=user,
            created_at=timestamp,
            updated_at=timestamp,
            is_deleted=False,
            is_archived=False,
            # Valeurs par défaut
            bio="",
            phone="",
            website="",
            linkedin_url="",
            github_url="",
            remote_work_preference="HYBRID",
            timezone="Europe/Paris",
            email_notifications=True,
            sms_notifications=False,
            notes=""
        )
        
        return profile
    
    @staticmethod
    def get_user_data(user):
        """
        Récupère toutes les données de l'utilisateur (profil, statistiques, etc.)
        """
        from apps.profiles.models import UserProfile, UserSettings
        
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            profile = ProfileService.create_empty_profile(user)
        
        try:
            settings = UserSettings.objects.get(profile=profile)
        except UserSettings.DoesNotExist:
            # Créer les paramètres par défaut
            settings = UserSettings.objects.create(
                id=str(uuid.uuid4()),
                profile=profile,
                user=user,
                created_at=int(time.time() * 1000),
                updated_at=int(time.time() * 1000),
                is_deleted=False,
                is_archived=False,
                theme="SYSTEM",
                timezone="Europe/Paris",
                notif_email=True,
                notif_push=True,
                dashboard_range=7
            )
        
        # Mettre à jour les statistiques
        ProfileService.update_stats(user)
        
        # Construire la réponse
        return {
            "profile": profile,
            "settings": settings
        }