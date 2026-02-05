"""
Cars URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ManufacturerViewSet, CarViewSet, dealership_settings_detail, dealership_settings_update
from .views import recently_sold_list, recently_sold_create, add_car_to_recently_sold

router = DefaultRouter()
router.register(r'manufacturers', ManufacturerViewSet, basename='manufacturer')
router.register(r'', CarViewSet, basename='car')

app_name = 'cars'

urlpatterns = [
    # Recently sold endpoints
    path('recently-sold/', recently_sold_list, name='recently-sold-list'),
    path('recently-sold/create/', recently_sold_create, name='recently-sold-create'),
    path('recently-sold/add-car/', add_car_to_recently_sold, name='add-car-to-recently-sold'),
    
    # Settings endpoints
    path('settings/', dealership_settings_detail, name='settings-detail'),
    path('settings/update/', dealership_settings_update, name='settings-update'),
    
    # Car and Manufacturer endpoints (via router) - MUST BE LAST
    path('', include(router.urls)),
]
