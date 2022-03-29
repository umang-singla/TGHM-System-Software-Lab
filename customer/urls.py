from django.urls import path, include
from . import views

app_name = 'customer'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('register_customer/', views.register_customer, name='register_customer'),
    path('login_customer/', views.login_customer, name='login_customer'),
    path('dashboard/<int:customer_id>',views.dashboard,name='dashboard'),
    path('dashboard/fetch_station/',views.fetch_station,name='fetch_station'),
    path('dashboard/fetch_food/', views.fetch_food, name='fetch_food'),
    path('dashboard/get_time/', views.get_time, name='get_time'),
    path('place_order/<int:customer_id>', views.place_order, name='place_order'),
    path('change_status/<int:order_id>', views.change_status, name='change_status'),
]