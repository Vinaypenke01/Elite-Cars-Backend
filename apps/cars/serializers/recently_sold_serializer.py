"""
Recently Sold Serializer
"""
from rest_framework import serializers
from apps.cars.models import RecentlySold


class RecentlySoldSerializer(serializers.ModelSerializer):
    """
    Serializer for RecentlySold model
    """
    class Meta:
        model = RecentlySold
        fields = ['id', 'car_name', 'price', 'sold_date', 'image', 'created_at']
        read_only_fields = ['created_at']
    
    def validate_sold_date(self, value):
        """Validate sold date is not in the future"""
        from datetime import date
        if value > date.today():
            raise serializers.ValidationError("Sold date cannot be in the future")
        return value
