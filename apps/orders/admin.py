"""
Orders Admin Configuration
"""
from django.contrib import admin
from .models import Booking, Enquiry


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['car_name', 'customer_name', 'email', 'date', 'time', 'status', 'created_at']
    list_filter = ['status', 'package_type', 'date', 'created_at']
    search_fields = ['car_name', 'customer_name', 'email', 'phone']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Car Information', {
            'fields': ('car', 'car_name', 'package_type')
        }),
        ('Customer Information', {
            'fields': ('customer_name', 'email', 'phone')
        }),
        ('Appointment Details', {
            'fields': ('date', 'time', 'message')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'email', 'phone', 'get_car_name', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'updated_at']
    search_fields = ['customer_name', 'email', 'phone', 'car__model_name', 'car__manufacturer__name']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    actions = ['mark_contacted', 'mark_converted', 'mark_closed']
    
    fieldsets = (
        ('Car Information', {
            'fields': ('car',)
        }),
        ('Customer Information', {
            'fields': ('customer_name', 'email', 'phone', 'message')
        }),
        ('Status & Notes', {
            'fields': ('status', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def get_car_name(self, obj):
        """Display formatted car name"""
        return f"{obj.car.manufacturer.name} {obj.car.model_name}"
    get_car_name.short_description = 'Car'
    
    @admin.action(description='Mark as Contacted')
    def mark_contacted(self, request, queryset):
        queryset.update(status='CONTACTED')
    
    @admin.action(description='Mark as Converted')
    def mark_converted(self, request, queryset):
        queryset.update(status='CONVERTED')
    
    @admin.action(description='Mark as Closed')
    def mark_closed(self, request, queryset):
        queryset.update(status='CLOSED')
