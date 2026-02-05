"""
Car Feature Model
"""
from django.db import models
from apps.cars.models.car import Car


class CarFeature(models.Model):
    """
    Model for storing individual car features
    """
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='features')
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'car_features'
        verbose_name = 'Car Feature'
        verbose_name_plural = 'Car Features'

    def __str__(self):
        return f"{self.name} - {self.car}"
