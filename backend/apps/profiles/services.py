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
            return
        
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