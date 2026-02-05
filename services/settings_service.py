"""
Settings Service
Business logic for dealership settings
"""
from apps.cars.models import DealershipSettings


class SettingsService:
    """Service class for dealership settings"""
    
    @staticmethod
    def get_settings():
        """Get dealership settings (singleton)"""
        return DealershipSettings.load()
    
    @staticmethod
    def update_settings(data):
        """Update dealership settings"""
        settings = DealershipSettings.load()
        
        for key, value in data.items():
            if hasattr(settings, key):
                setattr(settings, key, value)
        
        settings.save()
        return settings
