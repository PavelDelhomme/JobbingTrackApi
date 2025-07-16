from django.contrib import admin
from .models import Reference

@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('label', 'type', 'user', 'is_default', 'created_at')
    list_filter = ('type', 'is_default', 'created_at')
    search_fields = ('label', 'type')
    readonly_fields = ('id', 'created_at', 'updated_at')
