from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'user', 'created_at')
    list_filter = ('is_archived', 'is_deleted', 'created_at')
    search_fields = ('title', 'company_name')
    readonlue_fields = ('id', 'created_at', 'updated_at', 'sync_hash')
