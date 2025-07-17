from django.contrib import admin
from .models import Call

@admin.register(Call)
class CallAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'contact_name', 'user', 'created_at')
    list_filter = ('is_archived', 'is_deleted', 'created_at')
    search_fields = ('title', 'company_name', 'contact_name')
    readonly_fields = ('id', 'created_at', 'updated_at', 'sync_hash')
