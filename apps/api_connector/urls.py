from django.urls import path
from . import views

urlpatterns = [
    path('fake/kpis/<str:zone_code>/', views.fake_kpi_data, name='fake_kpi_data'),
    path('fake/kpis/<str:zone_code>/<str:kpi_type>/', views.fake_kpi_single, name='fake_kpi_single'),
]