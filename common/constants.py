"""
Common Constants for Elite Motors
"""

# Booking/Order Status
class BookingStatus:
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    
    CHOICES = [
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    ]

# Package Types
class PackageType:
    BASIC = 'basic'
    PREMIUM = 'premium'
    ULTIMATE = 'ultimate'
    
    CHOICES = [
        (BASIC, 'Basic'),
        (PREMIUM, 'Premium'),
        (ULTIMATE, 'Ultimate'),
    ]

# Car Types
class CarType:
    ELECTRIC = 'Electric'
    ELECTRIC_LUXURY = 'Electric Luxury'
    ELECTRIC_SUV = 'Electric SUV'
    ELECTRIC_SPORTS = 'Electric Sports'
    
    CHOICES = [
        (ELECTRIC, 'Electric'),
        (ELECTRIC_LUXURY, 'Electric Luxury'),
        (ELECTRIC_SUV, 'Electric SUV'),
        (ELECTRIC_SPORTS, 'Electric Sports'),
    ]

# Admin Roles
class AdminRole:
    ADMIN = 'admin'
    SUPER_ADMIN = 'super_admin'
    
    CHOICES = [
        (ADMIN, 'Admin'),
        (SUPER_ADMIN, 'Super Admin'),
    ]

# Package Prices
PACKAGE_PRICES = {
    PackageType.BASIC: 100,
    PackageType.PREMIUM: 250,
    PackageType.ULTIMATE: 500,
}

# API Response Messages
class Messages:
    # Success messages
    SUCCESS = "Operation successful"
    CREATED = "Resource created successfully"
    UPDATED = "Resource updated successfully"
    DELETED = "Resource deleted successfully"
    
    # Auth messages
    LOGIN_SUCCESS = "Login successful"
    LOGOUT_SUCCESS = "Logged out successfully"
    REGISTER_SUCCESS = "Registration successful"
    INVALID_CREDENTIALS = "Invalid credentials"
    UNAUTHORIZED = "Unauthorized access"
    
    # Error messages
    NOT_FOUND = "Resource not found"
    BAD_REQUEST = "Bad request"
    SERVER_ERROR = "Internal server error"
    VALIDATION_ERROR = "Validation error"
    
    # Booking messages
    BOOKING_CREATED = "Booking created successfully"
    BOOKING_UPDATED = "Booking updated successfully"
    BOOKING_CANCELLED = "Booking cancelled successfully"
    
    # Car messages
    CAR_CREATED = "Car added successfully"
    CAR_UPDATED = "Car updated successfully"
    CAR_DELETED = "Car deleted successfully"
