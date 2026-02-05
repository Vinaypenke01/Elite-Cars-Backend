"""
Admin Profile Model
"""
from django.db import models
from django.contrib.auth.models import User
from common.constants import AdminRole


class AdminProfile(models.Model):
    """
    Extended profile for admin users
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='admin_profile'
    )
    role = models.CharField(
        max_length=20,
        choices=AdminRole.CHOICES,
        default=AdminRole.ADMIN
    )
    display_name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'admin_profiles'
        verbose_name = 'Admin Profile'
        verbose_name_plural = 'Admin Profiles'
    
    def __str__(self):
        return f"{self.user.email} - {self.get_role_display()}"
    
    @property
    def uid(self):
        """Return user ID for compatibility"""
        return self.user.id
    
    @property
    def email(self):
        """Return user email"""
        return self.user.email
