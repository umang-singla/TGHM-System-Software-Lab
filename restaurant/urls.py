from django.urls import path, include
from . import views

app_name = 'restaurant'

urlpatterns = [
    # path('', views.login, name='login')
    path('login/', views.login, name='login'),
    path('dashboard/<int:restaurant_id>', views.dashboard, name='dashboard'),
    path('login_restaurant/', views.login_restaurant, name='login_restaurant'),
    path('register/', views.register, name='register'),
    path('register_restaurant/', views.register_restaurant, name='register_restaurant'),
    path('add_food/<int:restaurant_id>', views.add_food, name='add_food'),
    path('change_status/<int:order_id>', views.change_status, name='change_status'),
]