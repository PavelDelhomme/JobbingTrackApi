from django.utils import timezone
from django.db.models import Count
from apps.applications.models import Application
from apps.calls.models import Call
from apps.followups.models import FollowUp
from apps.interviews.models import Interview
from apps.profiles.models import UserProfile, UserSettings


class ProfileService:
    @staticmethod
    def refresh_stats(profile: UserProfile):
        since = timezone.now() - timezone.timedelta(days=7)
        profile.apps_last_7 = Application.objects.filter(
            user=profile.user, created_at__gte=since).count()
        profile.calls_last_7 = Call.objects.filter(
            user=profile.user, created_at__gte=since).count()
        profile.fu_last_7 = FollowUp.objects.filter(
            user=profile.user, created_at__gte=since).count()
        profile.itw_last_7 = Interview.objects.filter(
            user=profile.user, created_at__gte=since).count()
        profile.save(update_fields=[
            'apps_last_7', 'calls_last_7', 'fu_last_7', 'itw_last_7'
        ])

    @staticmethod
    def get_dashboard(profile: UserProfile):
        settings = profile.settings
        return {
            "range": settings.dashboard_range,
            "stats": {
                "applications": profile.apps_last_7,
                "calls": profile.calls_last_7,
                "followups": profile.fu_last_7,
                "interviews": profile.itw_last_7,
            }
        }
