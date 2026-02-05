"""
Orders URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookingViewSet, EnquiryViewSet

router = DefaultRouter()
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'enquiries', EnquiryViewSet, basename='enquiry')

app_name = 'orders'

urlpatterns = [
    path('', include(router.urls)),
]
