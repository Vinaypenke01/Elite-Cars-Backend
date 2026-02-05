"""
Car Model
"""
from django.db import models
from apps.cars.models.manufacturer import Manufacturer


class Car(models.Model):
    """
    Car model for vehicle inventory - Comprehensive dealer system
    """

    FUEL_CHOICES = [
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
        ('CNG', 'CNG'),
        ('Electric', 'Electric'),
    ]

    TRANSMISSION_CHOICES = [
        ('Manual', 'Manual'),
        ('Automatic', 'Automatic'),
        ('AMT', 'AMT'),
        ('CVT', 'CVT'),
    ]

    OWNER_CHOICES = [
        ('1st Owner', '1st Owner'),
        ('2nd Owner', '2nd Owner'),
        ('3rd Owner', '3rd Owner'),
    ]

    CONDITION_CHOICES = [
        ('Excellent', 'Excellent'),
        ('Good', 'Good'),
        ('Average', 'Average'),
    ]

    BODY_TYPE_CHOICES = [
        ('Hatchback', 'Hatchback'),
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('MUV', 'MUV'),
        ('Coupe', 'Coupe'),
        ('Convertible', 'Convertible'),
        ('Pickup', 'Pickup'),
    ]

    # 🔗 Manufacturer
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
        related_name='cars'
    )

    # 🔽 Dropdown Body Type
    body_type = models.CharField(
        max_length=20,
        choices=BODY_TYPE_CHOICES
    )

    # 🏷️ Identity
    model_name = models.CharField(max_length=50)
    variant = models.CharField(max_length=50, blank=True)

    model_year = models.PositiveIntegerField()
    registration_year = models.PositiveIntegerField()
    ownership = models.CharField(max_length=20, choices=OWNER_CHOICES)

    # 🚘 Specs
    kilometers_driven = models.PositiveIntegerField()
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    engine_cc = models.PositiveIntegerField()
    mileage = models.DecimalField(max_digits=5, decimal_places=2)
    color = models.CharField(max_length=30)

    # 💰 Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_negotiable = models.BooleanField(default=True)

    # 📄 Documents
    insurance_valid_till = models.DateField(null=True, blank=True)
    rc_available = models.BooleanField(default=True)
    puc_available = models.BooleanField(default=True)
    loan_clearance = models.BooleanField(default=True)

    # 🛠️ Condition
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    accident_history = models.BooleanField(default=False)
    service_history = models.BooleanField(default=True)

    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cars'
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.manufacturer.name} {self.model_name} ({self.model_year})"
