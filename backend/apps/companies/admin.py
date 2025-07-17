from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'sector', 'phone', 'email', 'user', 'created_at')
    list_filter = ('is_archived', 'is_deleted', 'sector', 'created_at')
    search_fields = ('name', 'sector', 'email')
    readonly_fields = ('id', 'created_at', 'updated_at', 'sync_hash')
