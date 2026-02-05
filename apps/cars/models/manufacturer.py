"""
Manufacturer Model
"""
from django.db import models


class Manufacturer(models.Model):
    """
    Manufacturer model for car brands
    """
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'manufacturers'
        verbose_name = 'Manufacturer'
        verbose_name_plural = 'Manufacturers'
        ordering = ['name']

    def __str__(self):
        return self.name
