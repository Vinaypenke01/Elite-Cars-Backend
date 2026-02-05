"""
Account Views
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from core.responses import success_response, error_response, created_response
from common.constants import Messages
from services.auth_service import AuthService
from .serializers import AdminRegistrationSerializer, AdminLoginSerializer, AdminProfileSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register a new admin user"""
    serializer = AdminRegistrationSerializer(data=request.data)
    
    if not serializer.is_valid():
        return error_response(
            message=Messages.VALIDATION_ERROR,
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        result = AuthService.register_admin(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            display_name=serializer.validated_data.get('display_name', ''),
            role=serializer.validated_data.get('role', 'admin')
        )
        
        return created_response(
            data=result,
            message=Messages.REGISTER_SUCCESS
        )
    except Exception as e:
        return error_response(
            message=str(e),
            status_code=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Login admin user"""
    serializer = AdminLoginSerializer(data=request.data)
    
    if not serializer.is_valid():
        return error_response(
            message=Messages.VALIDATION_ERROR,
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        result = AuthService.login_admin(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        
        return success_response(
            data=result,
            message=Messages.LOGIN_SUCCESS
        )
    except Exception as e:
        return error_response(
            message=Messages.INVALID_CREDENTIALS,
            status_code=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Logout admin user"""
    try:
        AuthService.logout_admin(request.user)
        return success_response(message=Messages.LOGOUT_SUCCESS)
    except Exception as e:
        return error_response(message=str(e))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """Get admin profile"""
    try:
        admin_profile = AuthService.get_admin_profile(request.user)
        serializer = AdminProfileSerializer(admin_profile)
        return success_response(data=serializer.data)
    except Exception as e:
        return error_response(
            message=Messages.NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND
        )
