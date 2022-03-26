from django.urls import path, include
from . import views

app_name = 'customer'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('register_customer/', views.register_customer, name='register_customer'),
    path('login_customer/', views.login_customer, name='login_customer'),
]