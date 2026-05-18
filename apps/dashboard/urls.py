from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('zone1/', views.zone1, name='zone1'),
    path('zone2/', views.zone2, name='zone2'),
    path('zone3/', views.zone3, name='zone3'),
    path('zone1/kpis/', views.zone1_kpis_partial, name='zone1_kpis'),
    path('zone1/history/<str:kpi_name>/', views.kpi_history, name='kpi_history'),
    path('zone1/export/csv/', views.export_csv, name='export_csv'),
    path('zone1/export/excel/', views.export_excel, name='export_excel'),
    path('zone1/comparison/', views.kpi_comparison, name='kpi_comparison'),
]