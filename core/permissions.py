"""
Custom Permissions for Elite Motors
"""
from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit objects.
    Read-only permissions are allowed for any request.
    """
    
    def has_permission(self, request, view):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to authenticated admin users
        return request.user and request.user.is_authenticated and hasattr(request.user, 'admin_profile')


class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admins.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and hasattr(request.user, 'admin_profile')


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow owners or admins to edit.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if user is admin
        if request.user and hasattr(request.user, 'admin_profile'):
            return True
        
        # Check if user is owner
        return obj.user == request.user
