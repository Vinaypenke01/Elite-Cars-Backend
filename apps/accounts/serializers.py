"""
Account Serializers
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import AdminProfile


class AdminProfileSerializer(serializers.ModelSerializer):
    """Serializer for admin profile"""
    uid = serializers.IntegerField(source='user.id', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = AdminProfile
        fields = ['uid', 'email', 'role', 'display_name', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class AdminRegistrationSerializer(serializers.Serializer):
    """Serializer for admin registration"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    display_name = serializers.CharField(required=False, allow_blank=True)
    role = serializers.ChoiceField(choices=AdminProfile._meta.get_field('role').choices, default='admin')
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists")
        return value


class AdminLoginSerializer(serializers.Serializer):
    """Serializer for admin login"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
