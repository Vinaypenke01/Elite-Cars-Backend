"""
Authentication Service
Business logic for user authentication
"""
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from apps.accounts.models import AdminProfile


class AuthService:
    """Service class for authentication operations"""
    
    @staticmethod
    def register_admin(email, password, display_name='', role='admin'):
        """Register a new admin user"""
        # Create user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )
        
        # Create admin profile
        admin_profile = AdminProfile.objects.create(
            user=user,
            role=role,
            display_name=display_name or email
        )
        
        # Generate token
        token, _ = Token.objects.get_or_create(user=user)
        
        return {
            'token': token.key,
            'user': {
                'uid': user.id,
                'email': user.email,
                'display_name': admin_profile.display_name,
                'role': admin_profile.role
            }
        }
    
    @staticmethod
    def login_admin(email, password):
        """Login admin user"""
        # Try to find user by email first
        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            username = email
            
        user = authenticate(username=username, password=password)
        
        if not user:
            raise ValueError("Invalid credentials")
        
        # Check if user has admin profile
        try:
            admin_profile = user.admin_profile
        except AdminProfile.DoesNotExist:
            # Auto-create profile for superusers
            if user.is_superuser:
                admin_profile = AdminProfile.objects.create(
                    user=user,
                    role='super_admin',
                    display_name='Super Admin'
                )
            else:
                raise ValueError("User is not an admin")
        
        # Get or create token
        token, _ = Token.objects.get_or_create(user=user)
        
        return {
            'token': token.key,
            'user': {
                'uid': user.id,
                'email': user.email,
                'display_name': admin_profile.display_name,
                'role': admin_profile.role
            }
        }
    
    @staticmethod
    def logout_admin(user):
        """Logout admin user by deleting token"""
        try:
            token = Token.objects.get(user=user)
            token.delete()
        except Token.DoesNotExist:
            pass
    
    @staticmethod
    def get_admin_profile(user):
        """Get admin profile for user"""
        return user.admin_profile
