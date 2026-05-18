from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('apps.authentication.urls')),
    path('backoffice/', include('apps.backoffice.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('api/', include('apps.api_connector.urls')),
    path('', lambda request: redirect('auth:login'), name='home'),
]