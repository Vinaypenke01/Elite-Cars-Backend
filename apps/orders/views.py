"""
Booking Views
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from core.permissions import IsAdmin
from core.responses import success_response, error_response, created_response
from common.constants import Messages
from .models import Booking, Enquiry
from .serializers import BookingSerializer, BookingCreateSerializer, EnquirySerializer


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Booking model
    List/retrieve bookings require admin auth
    Create booking is public
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
    def get_permissions(self):
        """Set permissions based on action"""
        if self.action == 'create':
            return [AllowAny()]
        return [IsAdmin()]
    
    def get_serializer_class(self):
        """Use different serializers for create"""
        if self.action == 'create':
            return BookingCreateSerializer
        return BookingSerializer
    
    def create(self, request, *args, **kwargs):
        """Create a new booking"""
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            booking = serializer.save()
            response_serializer = BookingSerializer(booking)
            return created_response(
                data=response_serializer.data,
                message=Messages.BOOKING_CREATED
            )
        
        return error_response(
            message=Messages.VALIDATION_ERROR,
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['patch'], permission_classes=[IsAdmin])
    def update_status(self, request, pk=None):
        """Update booking status (admin only)"""
        booking = self.get_object()
        new_status = request.data.get('status')
        
        if not new_status:
            return error_response(
                message="Status is required",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = new_status
        booking.save()
        
        serializer = self.get_serializer(booking)
        return success_response(
            data=serializer.data,
            message=Messages.BOOKING_UPDATED
        )


class EnquiryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Enquiry model
    Create is public, list/retrieve/update require admin
    """
    queryset = Enquiry.objects.select_related('car', 'car__manufacturer').all()
    serializer_class = EnquirySerializer
    
    def get_permissions(self):
        """Set permissions based on action"""
        if self.action == 'create':
            return [AllowAny()]
        return [IsAdmin()]
    
    def create(self, request, *args, **kwargs):
        """Create a new enquiry"""
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            enquiry = serializer.save()
            return created_response(
                data=EnquirySerializer(enquiry).data,
                message="Enquiry submitted successfully. We'll contact you soon!"
            )
        
        return error_response(
            message=Messages.VALIDATION_ERROR,
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['patch'], permission_classes=[IsAdmin])
    def update_status(self, request, pk=None):
        """Update enquiry status (admin only)"""
        enquiry = self.get_object()
        new_status = request.data.get('status')
        admin_notes = request.data.get('admin_notes')
        
        if new_status:
            enquiry.status = new_status
        if admin_notes is not None:
            enquiry.admin_notes = admin_notes
        
        enquiry.save()
        
        serializer = self.get_serializer(enquiry)
        return success_response(
            data=serializer.data,
            message="Enquiry updated successfully"
        )
