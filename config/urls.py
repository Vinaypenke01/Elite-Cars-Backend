"""
URL Configuration for Elite Motors Car Reseller Backend
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/v1/cars/', include('apps.cars.urls')),
    path('api/v1/accounts/', include('apps.accounts.urls')),
    path('api/v1/orders/', include('apps.orders.urls')),

    # Serve media and static files in production
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
