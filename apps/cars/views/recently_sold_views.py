"""
Recently Sold Views
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from core.permissions import IsAdmin
from core.responses import success_response, error_response, created_response
from common.constants import Messages
from services.car_service import CarService
from apps.cars.serializers import RecentlySoldSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def recently_sold_list(request):
    """Get recently sold cars"""
    try:
        limit = int(request.query_params.get('limit', 10))
        recently_sold = CarService.get_recently_sold(limit=limit)
        serializer = RecentlySoldSerializer(recently_sold, many=True)
        return success_response(data=serializer.data)
    except Exception as e:
        return error_response(message=str(e))


@api_view(['POST'])
@permission_classes([IsAdmin])
def recently_sold_create(request):
    """Add a recently sold car (admin only)"""
    serializer = RecentlySoldSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return created_response(
            data=serializer.data,
            message="Recently sold car added successfully"
        )
    
    return error_response(
        message=Messages.VALIDATION_ERROR,
        errors=serializer.errors,
        status_code=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
@permission_classes([IsAdmin])
def add_car_to_recently_sold(request):
    """Move a car to recently sold (admin only)"""
    try:
        car_id = request.data.get('car_id')
        sold_date = request.data.get('sold_date', None)
        
        if not car_id:
            return error_response(
                message="car_id is required",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # Add car to recently sold
        recently_sold = CarService.add_car_to_recently_sold(car_id, sold_date)
        serializer = RecentlySoldSerializer(recently_sold)
        
        return created_response(
            data=serializer.data,
            message="Car added to recently sold successfully"
        )
    except Exception as e:
        return error_response(
            message=str(e),
            status_code=status.HTTP_400_BAD_REQUEST
        )

