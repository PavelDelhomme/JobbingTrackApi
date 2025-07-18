# backend/logic/profile_service.py
from django.db.models import Count
from apps.applications.models import Application

class ProfileService:
    @staticmethod
    def stats_last_7_days(user):
        qs = Application.objects.filter(user=user, created_at__gte=timezone.now()-timezone.timedelta(days=7))
        return qs.aggregate(count=Count('id'))['count']
