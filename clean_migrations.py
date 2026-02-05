"""
Script to drop all tables and clear migration state for fresh start
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

# Drop all app tables
with connection.cursor() as cursor:
    tables = ['cars', 'car_images', 'car_features', 'manufacturers', 'bookings', 'recently_sold']
    for table in tables:
        try:
            cursor.execute(f"DROP TABLE IF EXISTS {table}")
            print(f"✓ Dropped table: {table}")
        except Exception as e:
            print(f"  Table {table} error: {e}")
    
    # Clear migration records for affected apps
    for app in ['cars', 'orders']:
        cursor.execute(f"DELETE FROM django_migrations WHERE app='{app}'")
        print(f"✓ Cleared {app} migration records")

print("\n✅ Ready for fresh migrations!")
print("Run: python manage.py makemigrations && python manage.py migrate")
