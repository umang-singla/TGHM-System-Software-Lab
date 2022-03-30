from django.test import TestCase
from django.http import HttpRequest
from restaurant.models import Restaurant, FoodItem
from restaurant.models import Station
from manager.models import Admin, Station
from restaurant.views import *

class RestaurentTestCase(TestCase):
    def setUp(self) -> None:
        # Create a restaurant
        # test_station = Station(name='Test Station')
        pass

    def test_register_restaurant_station_not_selected(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['name'] = 'Mera Restaurant'
        request.POST['username'] = 'Test Restaurant'
        request.POST['password'] = '123'
        request.POST['re_password'] = '123'
        request.POST['mobile'] = '123456789'
        request.POST['station'] = 'Test Address'


    def test_negative_price(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['name'] = 'Mera Restaurant'
        request.POST['username'] = 'Test Restaurant'
        request.POST['password'] = '123'
        request.POST['re_password'] = '123'
        request.POST['mobile'] = '123'


    
