"""
Accounts Admin Configuration
"""
from django.contrib import admin
from .models import AdminProfile


@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'display_name', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['user__email', 'display_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'role', 'display_name')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
