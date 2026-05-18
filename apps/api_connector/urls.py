from django.urls import path
from . import views

app_name = 'api_connector'

urlpatterns = [
    path('fake/kpis/<str:zone_code>/', views.fake_kpi_data, name='fake_kpis'),
    path('fake/kpis/<str:zone_code>/<str:kpi_type>/', views.fake_kpi_single, name='fake_kpi_single'),
]