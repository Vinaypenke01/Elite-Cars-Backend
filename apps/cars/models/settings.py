"""
Dealership Settings Model
"""
from django.db import models
from django.core.exceptions import ValidationError


class DealershipSettings(models.Model):
    """
    Singleton model for dealership settings
    """
    address = models.CharField(max_length=500)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    business_hours_mon_sat = models.CharField(max_length=50, default="9:00 AM - 8:00 PM")
    business_hours_sunday = models.CharField(max_length=50, default="10:00 AM - 6:00 PM")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'dealership_settings'
        verbose_name ='Dealership Settings'
        verbose_name_plural = 'Dealership Settings'
    
    def save(self, *args, **kwargs):
        """Ensure only one instance exists (singleton pattern)"""
        if not self.pk and DealershipSettings.objects.exists():
            raise ValidationError('Only one DealershipSettings instance is allowed')
        self.pk = 1
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        """Prevent deletion of settings"""
        raise ValidationError('Cannot delete dealership settings')
    
    @classmethod
    def load(cls):
        """Load the singleton instance"""
        obj, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'address': '123 Luxury Lane, Beverly Hills, CA 90210',
                'phone': '+1 (555) 123-4567',
                'email': 'info@elitecars.com'
            }
        )
        return obj
    
    def __str__(self):
        return f"Dealership Settings - {self.email}"
    
    @property
    def business_hours(self):
        """Return business hours as a dictionary"""
        return {
            'mon_sat': self.business_hours_mon_sat,
            'sunday': self.business_hours_sunday,
        }
