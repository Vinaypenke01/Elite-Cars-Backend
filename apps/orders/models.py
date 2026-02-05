"""
Booking Model
"""
from django.db import models
from apps.cars.models import Car
from common.constants import BookingStatus, PackageType
from common.validators import validate_phone, validate_booking_date


class Booking(models.Model):
    """
    Booking model for test drive appointments
    """
    # Car information
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    car_name = models.CharField(max_length=200)
    package_type = models.CharField(
        max_length=20,
        choices=PackageType.CHOICES
    )
    
    # Customer information
    customer_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, validators=[validate_phone])
    
    # Appointment details
    date = models.DateField(validators=[validate_booking_date])
    time = models.TimeField()
    message = models.TextField(blank=True)
    
    # Booking status
    status = models.CharField(
        max_length=20,
        choices=BookingStatus.CHOICES,
        default=BookingStatus.PENDING
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'bookings'
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.car_name} - {self.customer_name} ({self.date})"


class EnquiryStatus:
    """Enquiry status choices"""
    NEW = 'NEW'
    CONTACTED = 'CONTACTED'
    CONVERTED = 'CONVERTED'
    CLOSED = 'CLOSED'
    
    CHOICES = [
        (NEW, 'New'),
        (CONTACTED, 'Contacted'),
        (CONVERTED, 'Converted'),
        (CLOSED, 'Closed'),
    ]


class Enquiry(models.Model):
    """
    Enquiry model for customer enquiries about cars
    """
    # Car information
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='enquiries'
    )
    
    # Customer information
    customer_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, validators=[validate_phone])
    message = models.TextField(blank=True, help_text="Optional message from customer")
    
    # Enquiry status
    status = models.CharField(
        max_length=20,
        choices=EnquiryStatus.CHOICES,
        default=EnquiryStatus.NEW
    )
    
    # Admin notes
    admin_notes = models.TextField(blank=True, help_text="Internal notes for follow-up")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'enquiries'
        verbose_name = 'Enquiry'
        verbose_name_plural = 'Enquiries'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.customer_name} - {self.car} ({self.get_status_display()})"
