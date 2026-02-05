"""
Car Image Model
"""
from django.db import models
from apps.cars.models.car import Car


class CarImage(models.Model):
    """
    Model for storing car images as files
    """
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='cars/')
    is_primary = models.BooleanField(default=False)

    class Meta:
        db_table = 'car_images'
        verbose_name = 'Car Image'
        verbose_name_plural = 'Car Images'

    def __str__(self):
        return f"Image - {self.car}"
