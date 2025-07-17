from django.contrib import admin
from .models import Interview

@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_remote', 'tests_needed', 'tests_done', 'user', 'created_at')
    list_filter = ('is_remote', 'tests_needed', 'tests_done', 'salary_discussed', 'created_at')
    search_fields = ('title', 'location')
    readonly_fields = ('id', 'created_at', 'updated_at', 'sync_hash')
