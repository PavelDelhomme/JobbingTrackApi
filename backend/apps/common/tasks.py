from django.utils import timezone
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

def check_upcoming_interviews():    
    """
    Vérifie les entretiens à venir et envoie des notifications
    """
    from apps.interviews.models import Interview
    from apps.common.notification_service import NotificationService
    
    # Calculer les dates pour les entretiens de demain
    now = datetime.now()
    tomorrow = now + timedelta(days=1)
    tomorrow_start = int(datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0, 0).timestamp() * 1000)
    tomorrow_end = int(datetime(tomorrow.year, tomorrow.month, tomorrow.day, 23, 59, 59).timestamp() * 1000)
    
    # Récupérer les entretiens de demain
    interviews = Interview.objects.filter(
        interview_ts__gte=tomorrow_start,
        interview_ts__lte=tomorrow_end,
        is_deleted=False
    )
    
    for interview in interviews:
        NotificationService.notify_upcoming_interview(interview)
    
    logger.info(f"Vérification des entretiens terminée: {len(interviews)} notifications envoyées")

def check_pending_followups():
    """
    Vérifie les relances en attente et envoie des notifications
    """
    from apps.followups.models import FollowUp
    from apps.common.notification_service import NotificationService
    
    # Calculer le timestamp actuel
    now_ts = int(datetime.now().timestamp() * 1000)
    
    # Récupérer les relances en retard
    followups = FollowUp.objects.filter(
        followup_ts__lte=now_ts,
        is_completed=False,
        is_deleted=False
    )
    
    for followup in followups:
        NotificationService.notify_pending_followup(followup)
    
    logger.info(f"Vérification des relances terminée: {len(followups)} notifications envoyées")

def update_all_user_stats():
    """
    Met à jour les statistiques de tous les utilisateurs
    """
    from django.contrib.auth import get_user_model
    from apps.profiles.services import ProfileService
    
    User = get_user_model()
    users = User.objects.filter(is_active=True)
    
    for user in users:
        ProfileService.update_stats(user)
    
    logger.info(f"Mise à jour des statistiques terminée pour {len(users)} utilisateurs")