from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'related_object_type', 'is_completed', 'user', 'created_at')
    list_filter = ('related_object_type', 'is_completed', 'notification_enabled', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('id', 'created_at', 'updated_at', 'sync_hash')