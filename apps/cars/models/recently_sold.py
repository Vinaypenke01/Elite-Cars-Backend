"""
Recently Sold Model
"""
from django.db import models


class RecentlySold(models.Model):
    """
    Model to track recently sold vehicles
    """
    car_name = models.CharField(max_length=200)
    price = models.CharField(max_length=50)
    sold_date = models.DateField()
    image = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'recently_sold'
        verbose_name = 'Recently Sold'
        verbose_name_plural = 'Recently Sold'
        ordering = ['-sold_date', '-created_at']
    
    def __str__(self):
        return f"{self.car_name} - Sold on {self.sold_date}"
