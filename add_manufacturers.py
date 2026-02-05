"""
Script to populate initial manufacturers
Run with: python manage.py shell < add_manufacturers.py
"""
from apps.cars.models import Manufacturer

manufacturers_data = [
    {"name": "Maruti Suzuki", "country": "India"},
    {"name": "Hyundai", "country": "South Korea"},
    {"name": "Tata Motors", "country": "India"},
    {"name": "Mahindra", "country": "India"},
    {"name": "Honda", "country": "Japan"},
    {"name": "Toyota", "country": "Japan"},
    {"name": "Kia", "country": "South Korea"},
    {"name": "Volkswagen", "country": "Germany"},
    {"name": "Renault", "country": "France"},
    {"name": "Nissan", "country": "Japan"},
    {"name": "Ford", "country": "USA"},
    {"name": "Skoda", "country": "Czech Republic"},
    {"name": "MG Motor", "country": "UK"},
    {"name": "Jeep", "country": "USA"},
]

for data in manufacturers_data:
    manufacturer, created = Manufacturer.objects.get_or_create(**data)
    if created:
        print(f"✓ Created: {manufacturer.name}")
    else:
        print(f"- Already exists: {manufacturer.name}")

print(f"\n✅ Total manufacturers: {Manufacturer.objects.count()}")
