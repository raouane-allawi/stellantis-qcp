from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.shortcuts import render

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('apps.authentication.urls')),
    path('backoffice/', include('apps.backoffice.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('api/', include('apps.api_connector.urls')),
    path('', lambda request: redirect('auth:login'), name='home'),
]


def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)


def handler500(request):
    return render(request, 'errors/500.html', status=500)