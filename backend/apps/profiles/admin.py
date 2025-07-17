from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'remote_work_preference', 'email_notifications', 'created_at')
    list_filter = ('remote_work_preference', 'email_notifications', 'sms_notifications', 'created_at')
    search_fields = ('user__email', 'phone', 'bio')
    readonly_fields = ('id', 'created_at', 'updated_at', 'sync_hash')