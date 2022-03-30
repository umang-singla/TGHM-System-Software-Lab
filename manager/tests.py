from django.test import TestCase
from django.http import HttpRequest
from manager.models import Admin, Station, Train
from manager.views import *

class AdminTestCase(TestCase):
    def setUp(self) -> None:
        # Create Admin object
        self.admin = Admin.objects.create(username="admin", password="123")

    def test_incorrect_password(self):
        request = HttpRequest()
        request.method = "POST"
        request.POST['username'] = "admin"
        request.POST['password'] = "321"
        request._messages = messages.storage.default_storage(request)
        response = login_admin(request)
        assert(response.status_code == 302)
    
    def test_incorrect_username(self):
        request = HttpRequest()
        request.method = "POST"
        request.POST['username'] = "adnim"
        request.POST['password'] = "123"
        request._messages = messages.storage.default_storage(request)
        response = login_admin(request)
        assert(response.status_code == 302)

    def test_incorrect_username_password(self):
        request = HttpRequest()
        request.method = "POST"
        request.POST['username'] = "adnim"
        request.POST['password'] = "321"
        request._messages = messages.storage.default_storage(request)
        response = login_admin(request)
        assert(response.status_code == 302)

    def test_correct_username_password(self):
        request = HttpRequest()
        request.method = "POST"
        request.POST['username'] = "admin"
        request.POST['password'] = "123"
        request._messages = messages.storage.default_storage(request)
        response = login_admin(request)
        assert(response.status_code == 200)

class StationTestCase(TestCase):
    def setUp(self) -> None:
        # Create a Admin object
        self.station = Station.objects.create(name="Kharagpur", lat="-200", lng="40")

    def test_lattitude_out_of_range(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['station'] = "Kharagpur"
        request.POST['lat'] = "200"
        request.POST['lon'] = "30"
        request._messages = messages.storage.default_storage(request)
        response = add_station(request)
        assert(response.status_code == 302)

    def test_longitude_out_of_range(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['station'] = "Kharagpur"
        request.POST['lat'] = "30"
        request.POST['lon'] = "200"
        request._messages = messages.storage.default_storage(request)
        response = add_station(request)
        assert(response.status_code == 302)

    def test_input_string_valid(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['station'] = "Kharagpur"
        request.POST['lat'] = "$#%"
        request.POST['lon'] = "*&"
        request._messages = messages.storage.default_storage(request)
        response = add_station(request)
        assert(response.status_code == 302)

    def test_input_correct(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['station'] = "Kharagpur"
        request.POST['lat'] = "30"
        request.POST['lon'] = "40"
        request._messages = messages.storage.default_storage(request)
        response = add_station(request)
        assert(response.status_code == 200)