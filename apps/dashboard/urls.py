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
    path('zone2/kpis/', views.zone2_kpis_partial, name='zone2_kpis'),
    path('zone3/kpis/', views.zone3_kpis_partial, name='zone3_kpis'),
    path('zone1/history/<str:kpi_name>/', views.kpi_history, name='kpi_history'),
    path('zone2/history/<str:kpi_name>/', views.kpi_history, name='kpi_history_z2'),
    path('zone3/history/<str:kpi_name>/', views.kpi_history, name='kpi_history_z3'),
    path('zone1/export/csv/', views.export_csv, name='export_csv'),
    path('zone1/export/excel/', views.export_excel, name='export_excel'),
    path('zone2/export/csv/', views.export_csv, name='export_csv_z2'),
    path('zone2/export/excel/', views.export_excel, name='export_excel_z2'),
    path('zone3/export/csv/', views.export_csv, name='export_csv_z3'),
    path('zone3/export/excel/', views.export_excel, name='export_excel_z3'),
    path('zone1/comparison/', views.kpi_comparison, name='kpi_comparison'),
    path('zone2/comparison/', views.kpi_comparison, name='kpi_comparison_z2'),
    path('zone3/comparison/', views.kpi_comparison, name='kpi_comparison_z3'),
]