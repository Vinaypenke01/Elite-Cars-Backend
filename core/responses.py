"""
Custom API Response Utilities
"""
from rest_framework.response import Response
from rest_framework import status


def success_response(data=None, message="Success", status_code=status.HTTP_200_OK):
    """
    Standard success response format
    """
    response_data = {
        'success': True,
        'message': message,
    }
    if data is not None:
        response_data['data'] = data
    
    return Response(response_data, status=status_code)


def error_response(message="An error occurred", errors=None, status_code=status.HTTP_400_BAD_REQUEST):
    """
    Standard error response format
    """
    response_data = {
        'success': False,
        'message': message,
    }
    if errors:
        response_data['errors'] = errors
    
    return Response(response_data, status=status_code)


def created_response(data=None, message="Resource created successfully"):
    """
    Standard creation success response
    """
    return success_response(data=data, message=message, status_code=status.HTTP_201_CREATED)


def deleted_response(message="Resource deleted successfully"):
    """
    Standard deletion success response
    """
    return success_response(message=message, status_code=status.HTTP_204_NO_CONTENT)
