"""
Dealership Settings Views
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from core.permissions import IsAdmin
from core.responses import success_response, error_response
from common.constants import Messages
from services.settings_service import SettingsService
from apps.cars.serializers import DealershipSettingsSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def dealership_settings_detail(request):
    """Get dealership settings"""
    try:
        settings = SettingsService.get_settings()
        serializer = DealershipSettingsSerializer(settings)
        return success_response(data=serializer.data)
    except Exception as e:
        return error_response(
            message=Messages.NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND
        )


@api_view(['PATCH', 'PUT'])
@permission_classes([IsAdmin])
def dealership_settings_update(request):
    """Update dealership settings (admin only)"""
    try:
        settings = SettingsService.get_settings()
        serializer = DealershipSettingsSerializer(
            settings,
            data=request.data,
            partial=True
        )
        
        if serializer.is_valid():
            # Update business hours if provided
            if 'business_hours' in request.data:
                business_hours = request.data['business_hours']
                if 'mon_sat' in business_hours:
                    settings.business_hours_mon_sat = business_hours['mon_sat']
                if 'sunday' in business_hours:
                    settings.business_hours_sunday = business_hours['sunday']
            
            serializer.save()
            return success_response(
                data=serializer.data,
                message=Messages.UPDATED
            )
        
        return error_response(
            message=Messages.VALIDATION_ERROR,
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return error_response(message=str(e))
