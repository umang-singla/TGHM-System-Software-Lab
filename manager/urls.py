from django.urls import path, include
from . import views

app_name = 'manager'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('register_admin/', views.register_admin, name='register_admin'),
    path('login_admin/', views.login_admin, name='login_admin'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_station/', views.add_station, name='add_station'),
    path('add_train/', views.add_train, name='add_train'),
    path('change_station_status/', views.change_station_status, name='change_station_status'),
    path('edit_train/<int:train_id>', views.edit_train, name='edit_train'),
    path('statistics/', views.statistics, name='statistics'),
]