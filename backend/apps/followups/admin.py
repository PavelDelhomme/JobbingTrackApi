from django.contrib import admin
from .models import FollowUp

@admin.register(FollowUp)
class FollowUpAdmin(admin.ModelAdmin):
    list_display = ('title', 'method', 'response_received', 'user', 'created_at')
    list_filter = ('method', 'response_received', 'is_archived', 'is_deleted', 'created_at')
    search_fields = ('title', 'notes')
    readonly_fields = ('id', 'created_at', 'updated_at', 'sync_hash')