from django.test import TestCase
from django.http import HttpRequest
from restaurant.models import Restaurant, FoodItem
from restaurant.models import Station
from manager.models import Admin, Station
from restaurant.views import *

class RestaurentTestCase(TestCase):
    def setUp(self) -> None:
        # Create a station  
        self.station = Station.objects.create(name='Test Station', lat="23", lng="32")

    def test_register_restaurant_null_username(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['name'] = "Mera Restaurant"
        request.POST['username'] = ""
        request.POST['password'] = '123'
        request.POST['re_password'] = '123'
        request.POST['mobile'] = '123456789'
        station_id = self.station.id
        request.POST['station'] = station_id
        request._messages = messages.storage.default_storage(request)
        response = register_restaurant(request)
        assert(response.status_code, 302)

    def test_register_restaurant_null_password(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['name'] = "Mera Restaurant"
        request.POST['username'] = "Test Restaurent"
        request.POST['password'] = ""
        request.POST['re_password'] = '123'
        request.POST['mobile'] = '123456789'
        station_id = self.station.id
        request.POST['station'] = station_id
        request._messages = messages.storage.default_storage(request)
        response = register_restaurant(request)
        assert(response.status_code, 302)  

    def test_register_restaurent_repassword_mismatch(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['name'] = "Mera Restaurant"
        request.POST['username'] = "Test Restaurent"
        request.POST['password'] = '123'
        request.POST['re_password'] = '1234'
        request.POST['mobile'] = '123456789'
        station_id = self.station.id
        request.POST['station'] = station_id
        request._messages = messages.storage.default_storage(request)
        response = register_restaurant(request)
        assert(response.status_code, 302)

    def test_register_restaurant_success(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['name'] = "Mera Restaurant"
        request.POST['username'] = "Test Restaurent"
        request.POST['password'] = '123'
        request.POST['re_password'] = '123'
        request.POST['mobile'] = '123456789'
        station_id = self.station.id
        request.POST['station'] = station_id
        request._messages = messages.storage.default_storage(request)
        response = register_restaurant(request)
        assert(response.status_code, 200)  

    def test_login_restaurent_success(self):
        self.test_register_restaurant_success()
        request = HttpRequest()
        request.method = 'POST'
        request.POST['username'] = "Test Restaurent"
        request.POST['password'] = '123'
        request._messages = messages.storage.default_storage(request)
        response = login_restaurant(request)
        assert(response.status_code, 200)

    def test_login_restaurent_password_mismatch(self):
        self.test_register_restaurant_success()
        request = HttpRequest()
        request.method = 'POST'
        request.POST['username'] = "Test Restaurent"
        request.POST['password'] = '1234'
        request._messages = messages.storage.default_storage(request)
        response = login_restaurant(request)
        assert(response.status_code, 302)

    def test_login_restaurent_username_mismatch(self):
        self.test_register_restaurant_success()
        request = HttpRequest()
        request.method = 'POST'
        request.POST['username'] = "Testss Restaurent"
        request.POST['password'] = '123'
        request._messages = messages.storage.default_storage(request)
        response = login_restaurant(request)
        assert(response.status_code, 302)


    def test_negative_price(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['name'] = 'Mera Restaurant'
        request.POST['username'] = 'Test Restaurant'
        request.POST['password'] = '123'
        request.POST['re_password'] = '123'
        request.POST['mobile'] = '123'


    
