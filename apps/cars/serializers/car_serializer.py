"""
Car Serializer
"""
from rest_framework import serializers
from apps.cars.models import Manufacturer, Car, CarImage, CarFeature


class ManufacturerSerializer(serializers.ModelSerializer):
    """
    Serializer for Manufacturer model
    """
    class Meta:
        model = Manufacturer
        fields = ['id', 'name', 'country']


class CarImageSerializer(serializers.ModelSerializer):
    """
    Serializer for CarImage model
    """
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = CarImage
        fields = ['id', 'image', 'image_url', 'is_primary']
    
    def get_image_url(self, obj):
        """Get full URL for image"""
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            if request is not None:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class CarFeatureSerializer(serializers.ModelSerializer):
    """
    Serializer for CarFeature model
    """
    class Meta:
        model = CarFeature
        fields = ['id', 'name']


class CarSerializer(serializers.ModelSerializer):
    """
    Serializer for Car model
    """
    manufacturer_details = ManufacturerSerializer(source='manufacturer', read_only=True)
    manufacturer_id = serializers.PrimaryKeyRelatedField(
        queryset=Manufacturer.objects.all(),
        source='manufacturer',
        write_only=True
    )
    images = CarImageSerializer(many=True, read_only=True)
    features = CarFeatureSerializer(many=True, read_only=True)
    
    # Fields for creating features (write-only)
    feature_names = serializers.ListField(
        child=serializers.CharField(max_length=50),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Car
        fields = [
            'id',
            'manufacturer_details',
            'manufacturer_id',
            'body_type',
            'model_name',
            'variant',
            'model_year',
            'registration_year',
            'ownership',
            'kilometers_driven',
            'fuel_type',
            'transmission',
            'engine_cc',
            'mileage',
            'color',
            'price',
            'is_negotiable',
            'insurance_valid_till',
            'rc_available',
            'puc_available',
            'loan_clearance',
            'condition',
            'accident_history',
            'service_history',
            'description',
            'is_active',
            'created_at',
            'images',
            'features',
            'feature_names'
        ]
        read_only_fields = ['created_at', 'images', 'features']
    
    def create(self, validated_data):
        """Create car with features"""
        feature_names = validated_data.pop('feature_names', [])
        car = Car.objects.create(**validated_data)
        
        # Create features
        for feature_name in feature_names:
            CarFeature.objects.create(car=car, name=feature_name)
        
        return car
    
    def update(self, instance, validated_data):
        """Update car and features"""
        feature_names = validated_data.pop('feature_names', None)
        
        # Update car fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update features if provided
        if feature_names is not None:
            instance.features.all().delete()
            for feature_name in feature_names:
                CarFeature.objects.create(car=instance, name=feature_name)
        
        return instance


class CarListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for car listings
    """
    manufacturer_name = serializers.CharField(source='manufacturer.name', read_only=True)
    primary_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Car
        fields = [
            'id',
            'manufacturer_name',
            'model_name',
            'model_year',
            'price',
            'body_type',
            'fuel_type',
            'transmission',
            'kilometers_driven',
            'is_active',
            'primary_image'
        ]
    
    def get_primary_image(self, obj):
        """Get primary image URL"""
        primary_image = obj.images.filter(is_primary=True).first()
        if not primary_image:
            primary_image = obj.images.first()
        
        if primary_image:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(primary_image.image.url)
            return primary_image.image.url
        return None

