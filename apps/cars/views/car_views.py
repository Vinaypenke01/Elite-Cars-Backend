"""
Car Views
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from core.permissions import IsAdminOrReadOnly
from core.responses import success_response, error_response
from common.constants import Messages
from apps.cars.models import Manufacturer, Car, CarImage
from apps.cars.serializers import ManufacturerSerializer, CarSerializer, CarListSerializer
from services.car_service import CarService
import json


class ManufacturerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Manufacturer model
    """
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    permission_classes = [IsAdminOrReadOnly]


class CarViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Car model
    Provides CRUD operations for cars
    """
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    
    def get_serializer_class(self):
        """Use lightweight serializer for list view"""
        if self.action == 'list':
            return CarListSerializer
        return CarSerializer
    
    def get_queryset(self):
        """
        Filter cars by various criteria
        By default, only show active cars
        """
        user = self.request.user
        is_admin = user and user.is_authenticated
        
        queryset = Car.objects.select_related('manufacturer').prefetch_related('images', 'features')
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            active_bool = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=active_bool)
        elif not is_admin:
            # For non-admin users, only show active cars by default
            queryset = queryset.filter(is_active=True)
        
        # Filter by manufacturer
        manufacturer_id = self.request.query_params.get('manufacturer', None)
        if manufacturer_id:
            queryset = queryset.filter(manufacturer_id=manufacturer_id)
        
        # Filter by body type
        body_type = self.request.query_params.get('body_type', None)
        if body_type:
            queryset = queryset.filter(body_type=body_type)
        
        # Filter by fuel type
        fuel_type = self.request.query_params.get('fuel_type', None)
        if fuel_type:
            queryset = queryset.filter(fuel_type=fuel_type)
        
        # Filter by transmission
        transmission = self.request.query_params.get('transmission', None)
        if transmission:
            queryset = queryset.filter(transmission=transmission)
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        return queryset
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def featured(self, request):
        """Get featured/latest cars"""
        try:
            # Return latest 6 active cars
            cars = Car.objects.filter(is_active=True).order_by('-created_at')[:6]
            serializer = CarListSerializer(cars, many=True, context={'request': request})
            return success_response(data=serializer.data)
        except Exception as e:
            return error_response(message=str(e))
    
    def retrieve(self, request, *args, **kwargs):
        """Get car details with related cars"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        # Get related cars
        related_cars = CarService.get_related_cars(instance, limit=6)
        related_serializer = CarListSerializer(related_cars, many=True, context={'request': request})
        
        # Combine the data
        response_data = serializer.data
        response_data['related_cars'] = related_serializer.data
        
        return success_response(data=response_data)
    
    def _handle_images(self, car, images):
        """Helper to handle uploaded images"""
        if images:
            for index, image in enumerate(images):
                CarImage.objects.create(
                    car=car,
                    image=image,
                    is_primary=(index == 0)
                )

    def create(self, request, *args, **kwargs):
        """Create a new car"""
        data = dict(request.data.items())
        
        # Parse feature_names if it's a JSON string
        if 'feature_names' in data and isinstance(data['feature_names'], str):
            try:
                data['feature_names'] = json.loads(data['feature_names'])
            except json.JSONDecodeError:
                return error_response(
                    message="Invalid JSON in feature_names field",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            car = serializer.save()
            
            # Handle uploaded images
            images = request.FILES.getlist('uploaded_images')
            self._handle_images(car, images)
            
            return success_response(
                data=CarSerializer(car, context={'request': request}).data,
                message=Messages.CAR_CREATED,
                status_code=status.HTTP_201_CREATED
            )
        
        return error_response(
            message=Messages.VALIDATION_ERROR,
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    def update(self, request, *args, **kwargs):
        """Update a car"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        data = dict(request.data.items())
        
        # Parse feature_names if it's a JSON string
        if 'feature_names' in data and isinstance(data['feature_names'], str):
            try:
                data['feature_names'] = json.loads(data['feature_names'])
            except json.JSONDecodeError:
                pass

        serializer = self.get_serializer(instance, data=data, partial=partial)
        
        if serializer.is_valid():
            car = serializer.save()
            
            # Handle uploaded images if provided
            images = request.FILES.getlist('uploaded_images')
            if images:
                self._handle_images(car, images)
            
            return success_response(
                data=CarSerializer(car, context={'request': request}).data,
                message=Messages.CAR_UPDATED
            )
        return error_response(
            message=Messages.VALIDATION_ERROR,
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    def destroy(self, request, *args, **kwargs):
        """Delete a car"""
        instance = self.get_object()
        instance.delete()
        return success_response(
            message=Messages.CAR_DELETED,
            status_code=status.HTTP_204_NO_CONTENT
        )

