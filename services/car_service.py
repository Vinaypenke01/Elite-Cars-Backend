"""
Car Service
Business logic for car operations
"""
from apps.cars.models import Car, RecentlySold


class CarService:
    """Service class for car-related operations"""
    
    @staticmethod
    def get_all_cars(filters=None):
        """Get all cars with optional filters"""
        queryset = Car.objects.all()
        
        if filters:
            if 'type' in filters:
                queryset = queryset.filter(type=filters['type'])
            if 'featured' in filters:
                queryset = queryset.filter(featured=filters['featured'])
            if 'is_available' in filters:
                queryset = queryset.filter(is_available=filters['is_available'])
        
        return queryset
    
    @staticmethod
    def get_car_by_id(car_id):
        """Get a car by ID"""
        return Car.objects.get(pk=car_id)
    
    @staticmethod
    def get_featured_cars():
        """Get all featured cars"""
        return Car.objects.filter(featured=True, is_available=True)
    
    @staticmethod
    def create_car(data):
        """Create a new car"""
        return Car.objects.create(**data)
    
    @staticmethod
    def update_car(car_id, data):
        """Update a car"""
        car = Car.objects.get(pk=car_id)
        for key, value in data.items():
            setattr(car, key, value)
        car.save()
        return car
    
    @staticmethod
    def delete_car(car_id):
        """Delete a car"""
        car = Car.objects.get(pk=car_id)
        car.delete()
    
    @staticmethod
    def get_recently_sold(limit=10):
        """Get recently sold cars"""
        return RecentlySold.objects.all()[:limit]
    
    @staticmethod
    def add_recently_sold(data):
        """Add a recently sold car"""
        return RecentlySold.objects.create(**data)
    
    @staticmethod
    def add_car_to_recently_sold(car_id, sold_date=None):
        """Move a car to recently sold"""
        from datetime import date
        
        car = Car.objects.get(pk=car_id)
        
        # Use the first image from the car's images array
        image_url = car.images[0] if car.images else ""
        
        # Create recently sold entry
        recently_sold_data = {
            'car_name': car.name,
            'price': car.price,
            'sold_date': sold_date or date.today(),
            'image': image_url
        }
        
        recently_sold = RecentlySold.objects.create(**recently_sold_data)
        
        # Mark the car as unavailable so it doesn't show in current stock
        car.is_available = False
        car.save()
        
        return recently_sold
    
    @staticmethod
    def get_related_cars(car, limit=6):
        """
        Get related cars based on body type, manufacturer, and price range
        """
        from decimal import Decimal
        from django.db.models import Q
        
        # Calculate price range (±20% of current car price)
        price = Decimal(str(car.price))
        price_min = price * Decimal('0.8')
        price_max = price * Decimal('1.2')
        
        # Build query for related cars
        related_query = Q(is_active=True) & ~Q(id=car.id)  # Exclude current car
        
        # Priority 1: Same manufacturer AND same body type
        same_mfg_body = Car.objects.filter(
            related_query,
            manufacturer=car.manufacturer,
            body_type=car.body_type
        ).order_by('?')[:limit]
        
        # If we have enough, return them
        if same_mfg_body.count() >= limit:
            return same_mfg_body
        
        # Priority 2: Add cars with same manufacturer OR same body type
        related_cars = Car.objects.filter(
            related_query,
            Q(manufacturer=car.manufacturer) | Q(body_type=car.body_type),
            price__gte=price_min,
            price__lte=price_max
        ).select_related('manufacturer').prefetch_related('images', 'features').order_by('?')[:limit]
        
        # If still not enough, add any cars in similar price range
        if related_cars.count() < limit:
            additional = Car.objects.filter(
                related_query,
                price__gte=price_min,
                price__lte=price_max
            ).exclude(id__in=[c.id for c in related_cars]).select_related('manufacturer').prefetch_related('images', 'features').order_by('?')[:limit - related_cars.count()]
            
            related_cars = list(related_cars) + list(additional)
        
        return related_cars

