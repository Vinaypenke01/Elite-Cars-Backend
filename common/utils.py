"""
Common Utility Functions
"""
import re
from django.core.exceptions import ValidationError
from django.utils import timezone


def format_phone_number(phone):
    """
    Format phone number to standardcompatibility
    """
    # Remove all non-digit characters
    phone = re.sub(r'\D', '', phone)
    
    # Format as +1 (XXX) XXX-XXXX for US numbers
    if len(phone) == 10:
        return f"+1 ({phone[:3]}) {phone[3:6]}-{phone[6:]}"
    elif len(phone) == 11 and phone[0] == '1':
        return f"+{phone[0]} ({phone[1:4]}) {phone[4:7]}-{phone[7:]}"
    
    return phone


def validate_image_extension(value):
    """
    Validate that uploaded file is an image
    """
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    ext = value.name.lower().split('.')[-1]
    
    if f'.{ext}' not in valid_extensions:
        raise ValidationError(f'Unsupported file extension. Allowed: {", ".join(valid_extensions)}')


def generate_booking_reference():
    """
    Generate unique booking reference number
    """
    import uuid
    import time
    
    timestamp = str(int(time.time()))
    unique_id = str(uuid.uuid4())[:8]
    
    return f"BK-{timestamp}-{unique_id}".upper()


def calculate_booking_total(package_type):
    """
    Calculate total cost based on package type
    """
    from common.constants import PACKAGE_PRICES
    return PACKAGE_PRICES.get(package_type, 0)


def is_business_hours():
    """
    Check if current time is within business hours
    """
    now = timezone.now()
    current_time = now.time()
    current_day = now.weekday()  # 0 = Monday, 6 = Sunday
    
    # Business hours: Mon-Sat 9 AM - 8 PM, Sunday 10 AM - 6 PM
    if current_day == 6:  # Sunday
        return current_time.hour >= 10 and current_time.hour < 18
    else:  # Monday - Saturday
        return current_time.hour >= 9 and current_time.hour < 20


def slugify_car_name(name):
    """
    Convert car name to URL-friendly slug
    """
    import re
    from django.utils.text import slugify
    
    # Remove special characters and convert to slug
    slug = slugify(name)
    return slug


def format_currency(amount):
    """
    Format amount as currency
    """
    return f"${amount:,.2f}"


def get_client_ip(request):
    """
    Get client IP address from request
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
