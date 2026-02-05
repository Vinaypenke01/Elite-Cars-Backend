"""
Dealership Settings Serializer
"""
from rest_framework import serializers
from apps.cars.models import DealershipSettings


class DealershipSettingsSerializer(serializers.ModelSerializer):
    """
    Serializer for DealershipSettings model
    """
    business_hours = serializers.SerializerMethodField()
    
    class Meta:
        model = DealershipSettings
        fields = ['id', 'address', 'phone', 'email', 'business_hours', 'updated_at']
        read_only_fields = ['id', 'updated_at']
    
    def get_business_hours(self, obj):
        """Return business hours as a dictionary"""
        return {
            'mon_sat': obj.business_hours_mon_sat,
            'sunday': obj.business_hours_sunday,
        }
