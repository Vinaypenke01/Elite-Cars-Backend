"""
Booking Serializers
"""
from rest_framework import serializers
from .models import Booking, Enquiry
from apps.cars.serializers import CarListSerializer


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model"""
    car_details = CarListSerializer(source='car', read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'car', 'car_details', 'car_name', 'package_type',
            'customer_name', 'email', 'phone',
            'date', 'time', 'message',
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'car_details']
    
    def validate(self, data):
        """Validate booking data"""
        # Auto-populate car_name from car object
        if 'car' in data and not data.get('car_name'):
            car = data['car']
            data['car_name'] = f"{car.manufacturer.name} {car.model_name}"
        return data


class EnquirySerializer(serializers.ModelSerializer):
    """Serializer for Enquiry model"""
    car_details = CarListSerializer(source='car', read_only=True)
    car_name = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Enquiry
        fields = [
            'id', 'car', 'car_details', 'car_name',
            'customer_name', 'email', 'phone', 'message',
            'status', 'admin_notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'car_details', 'car_name', 'status', 'admin_notes']
    
    def get_car_name(self, obj):
        """Get formatted car name"""
        if obj.car:
            return f"{obj.car.manufacturer.name} {obj.car.model_name}"
        return "Unknown Car"


class BookingCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating bookings"""
    car_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'car_id', 'car_name', 'package_type',
            'customer_name', 'email', 'phone',
            'date', 'time', 'message'
        ]
    
    def create(self, validated_data):
        """Create booking with car reference"""
        from apps.cars.models import Car
        
        car_id = validated_data.pop('car_id')
        try:
            car = Car.objects.get(pk=car_id)
            validated_data['car'] = car
        except Car.DoesNotExist:
            raise serializers.ValidationError({"car_id": "Car not found"})
        
        return Booking.objects.create(**validated_data)
