from django.test import TestCase
from django.http import HttpRequest
from manager.models import Admin, Station, Train
from manager.views import *

class AdminTestCase(TestCase):
    def setUp(self) -> None:
        Admin.objects.create(username="admin", password="321")
        Admin.objects.create(username="adnim", password="123")
        Admin.objects.create(username="adnim", password="321")
        Admin.objects.create(username="admin", password="123")

    def test_correct_username(self):
        admin_123 = Admin.objects.get(username="admin", password="123")
        assert(admin_123.username == "admin")
       
    def test_correct_password(self):
        admin_123 = Admin.objects.get(username="admin", password="123")
        assert(admin_123.password == "123")

    def test_incorrect_username(self):
        adnim_123 = Admin.objects.get(username="adnim", password="123")
        assert(adnim_123.username == "adnim")

    def test_incorrect_password(self):
        admin_321 = Admin.objects.get(username="admin", password="321")
        assert(admin_321.password == "321")

class StationTestCase(TestCase):
    def setUp(self) -> None:
        # Create a Admin object
        self.admin = Admin.objects.create(username="admin", password="321")
        Station.objects.create(name="Kharagpur", lat="-200", lng="40")
        Station.objects.create(name="Kharagpur", lat="37.895", lng="1080")
        # Station.objects.create(name="Kharagpur", lat="$##$", lng="^$*@(")
        Station.objects.create(name="Kharagpur", lat="22.330", lng="87.323")

    def test_lattitude_out_of_range(self):
        kharagpur = Station.objects.get(name="Kharagpur", lat="-200", lng="40")
        request = HttpRequest()
        request.method = 'POST'
        request.POST['station'] = 'Kharagpur'
        request.POST['lat'] = '-200'
        request.POST['lon'] = '40'
        request._messages = messages.storage.default_storage(request)
        response = add_station(request)
        assert(response.status_code == 302)

    def test_lnggitude_out_of_range(self):
        kharagpur = Station.objects.get(name="Kharagpur", lat="37.895", lng="1080")
        # assert(kharagpur.lng > -180 and kharagpur.lng < 180)