from django.contrib import admin
from api.common.models import UserProfile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "get_subject", "get_user")

    def get_user(self, obj):
        relation = UserProfile.objects.filter(profile_id=obj.id).first()
        return relation.user_id if relation else None
    get_user.short_description = "User"
        
    def get_subject(self, obj):
        return obj.subject if hasattr(obj, "subject") else "-"
    get_subject.short_description = "Sujet"

admin.site.register(UserProfile, ProfileAdmin)