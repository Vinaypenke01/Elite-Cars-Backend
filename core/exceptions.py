"""
Custom Exception Handlers
"""
from rest_framework.views import exception_handler
from rest_framework import status
from django.core.exceptions import ValidationError
from django.http import Http404


def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF
    Returns error responses in a consistent format
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # Now add the HTTP status code to the response
    if response is not None:
        response.data['success'] = False
        response.data['status_code'] = response.status_code
        
        # Customize error message format
        if 'detail' in response.data:
            response.data['message'] = response.data.pop('detail')
        else:
            response.data['message'] = "An error occurred"
        
        # Handle validation errors
        if isinstance(exc, ValidationError):
            response.data['errors'] = response.data.pop('detail', {})
    
    # Handle 404 errors
    elif isinstance(exc, Http404):
        response = {
            'success': False,
            'message': 'Resource not found',
            'status_code': status.HTTP_404_NOT_FOUND
        }
    
    return response


class APIException(Exception):
    """
    Base API Exception
    """
    default_detail = 'A server error occurred.'
    default_code = 'error'
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    
    def __init__(self, detail=None, code=None, status_code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code
        if status_code is not None:
            self.status_code = status_code
        
        self.detail = detail
        self.code = code


class NotFoundException(APIException):
    """
    Exception for resource not found
    """
    default_detail = 'Resource not found'
    default_code = 'not_found'
    status_code = status.HTTP_404_NOT_FOUND


class BadRequestException(APIException):
    """
    Exception for bad requests
    """
    default_detail = 'Bad request'
    default_code = 'bad_request'
    status_code = status.HTTP_400_BAD_REQUEST


class UnauthorizedException(APIException):
    """
    Exception for unauthorized access
    """
    default_detail = 'Unauthorized access'
    default_code = 'unauthorized'
    status_code = status.HTTP_401_UNAUTHORIZED


class ForbiddenException(APIException):
    """
    Exception for forbidden access
    """
    default_detail = 'Forbidden'
    default_code = 'forbidden'
    status_code = status.HTTP_403_FORBIDDEN
