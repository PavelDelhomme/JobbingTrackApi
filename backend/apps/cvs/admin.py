from django.contrib import admin
from .models import Cv

@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_primary', 'user', 'created_at')
    list_filter = ('is_primary', 'is_archived', 'is_deleted', 'created_at')
    search_fields = ('title',)
    readonly_fields = ('id', 'created_at', 'updated_at', 'sync_hash')
