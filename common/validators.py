"""
Common Validators
"""
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
import re


def validate_phone(value):
    """
    Validate phone number format
    """
    # Remove all non-digit characters
    phone_number = re.sub(r'\D', '', value)
    
    # Check if it has valid length (10 or 11 digits)
    if len(phone_number) < 10 or len(phone_number) > 11:
        raise ValidationError("Phone number must be 10 or 11 digits")
    
    return value


def validate_positive_number(value):
    """
    Validate that number is positive
    """
    if value <= 0:
        raise ValidationError("Value must be greater than zero")
    
    return value


def validate_email_domain(value):
    """
    Validate email and check for common domains
    """
    # First validate email format
    email_validator = EmailValidator()
    email_validator(value)
    
    # Optionally check for disposable email domains
    disposable_domains = ['tempmail.com', '10minutemail.com', 'guerrillamail.com']
    domain = value.split('@')[1].lower()
    
    if domain in disposable_domains:
        raise ValidationError("Please use a permanent email address")
    
    return value


def validate_car_price(value):
    """
    Validate car price is within reasonable range
    """
    MIN_PRICE = 1000
    MAX_PRICE = 1000000
    
    if value < MIN_PRICE or value > MAX_PRICE:
        raise ValidationError(f"Price must be between ${MIN_PRICE:,} and ${MAX_PRICE:,}")
    
    return value


def validate_year(value):
    """
    Validate car year
    """
    from datetime import datetime
    current_year = datetime.now().year
    
    if value < 2000 or value > current_year + 1:
        raise ValidationError(f"Year must be between 2000 and {current_year + 1}")
    
    return value


def validate_booking_date(value):
    """
    Validate booking date is in the future
    """
    from datetime import date
    
    if value < date.today():
        raise ValidationError("Booking date must be in the future")
    
    return value


def validate_image_size(value):
    """
    Validate image file size (max 5MB)
    """
    MAX_SIZE_MB = 5
    MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024
    
    if value.size > MAX_SIZE_BYTES:
        raise ValidationError(f"Image size must be less than {MAX_SIZE_MB}MB")
    
    return value
