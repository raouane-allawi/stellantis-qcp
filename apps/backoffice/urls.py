from django.urls import path
from . import views

app_name = 'backoffice'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard_view'),
    path('users/', views.users_list, name='users_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/edit/', views.user_edit, name='user_edit'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),
    path('zones/', views.zones_list, name='zones_list'),
    path('zones/<int:zone_pk>/assign/', views.zone_assign_user, name='zone_assign_user'),
    path('logs/', views.logs_list, name='logs_list'),
]