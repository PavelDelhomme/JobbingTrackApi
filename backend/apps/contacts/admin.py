from django.contrib import admin
from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'company_name', 'user', 'created_at', 'phone')
    list_filter = ('is_archived', 'is_deleted', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'company_name', 'phone')
    readonly_fields = ('id', 'created_at', 'updated_at', 'sync_hash')