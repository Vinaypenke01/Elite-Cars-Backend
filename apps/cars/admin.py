"""
Cars Admin Configuration
"""
from django.contrib import admin
from .models import Manufacturer, Car, CarImage, CarFeature, DealershipSettings, RecentlySold


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']
    search_fields = ['name', 'country']
    ordering = ['name']


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1


class CarFeatureInline(admin.TabularInline):
    model = CarFeature
    extra = 1


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['manufacturer', 'model_name', 'model_year', 'price', 'body_type', 'fuel_type', 'is_active', 'created_at']
    list_filter = ['manufacturer', 'body_type', 'fuel_type', 'transmission', 'condition', 'is_active', 'created_at']
    search_fields = ['model_name', 'variant', 'description']
    list_editable = ['is_active']
    readonly_fields = ['created_at']
    inlines = [CarImageInline, CarFeatureInline]
    
    fieldsets = (
        ('Identity', {
            'fields': ('manufacturer', 'model_name', 'variant', 'body_type')
        }),
        ('Years & Ownership', {
            'fields': ('model_year', 'registration_year', 'ownership')
        }),
        ('Specifications', {
            'fields': ('kilometers_driven', 'fuel_type', 'transmission', 'engine_cc', 'mileage', 'color')
        }),
        ('Pricing', {
            'fields': ('price', 'is_negotiable')
        }),
        ('Documents', {
            'fields': ('insurance_valid_till', 'rc_available', 'puc_available', 'loan_clearance')
        }),
        ('Condition', {
            'fields': ('condition', 'accident_history', 'service_history')
        }),
        ('Additional Info', {
            'fields': ('description', 'is_active', 'created_at')
        }),
    )


@admin.register(DealershipSettings)
class DealershipSettingsAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone', 'updated_at']
    readonly_fields = ['updated_at']
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not DealershipSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion
        return False


@admin.register(RecentlySold)
class RecentlySoldAdmin(admin.ModelAdmin):
    list_display = ['car_name', 'price', 'sold_date', 'created_at']
    list_filter = ['sold_date', 'created_at']
    search_fields = ['car_name']
    readonly_fields = ['created_at']
    ordering = ['-sold_date']
