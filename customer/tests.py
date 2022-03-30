from django.test import TestCase
from django.http import HttpRequest
from customer.views import * 
from customer.models import Customer, Orders

class CustomerTestCase(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(username='mradul', password='123')

    def test_customer_creation(self):
        self.assertTrue(isinstance(self.customer, Customer))

    def test_correct_login(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['username'] = 'mradul'
        request.POST['password'] = '123'
        request._messages = messages.storage.default_storage(request)
        response = login(request)
        assert(response.status_code, 200)
    
    def test_incorrect_login(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['username'] = 'mradulag'
        request.POST['password'] = '1234'
        request._messages = messages.storage.default_storage(request)
        response = login(request)
        assert(response.status_code, 302)

    def test_register_customer_success(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['username'] = 'mradulagrawal'
        request.POST['password'] = '12345'
        request.POST['re_password'] = '12345'
        request.POST['phone_number'] = '123456789'
        request._messages = messages.storage.default_storage(request)
        response = register_customer(request)
        assert(response.status_code, 200)

    def test_register_customer_unequal_password(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['username'] = 'mradulagrawal'
        request.POST['password'] = '12345'
        request.POST['re_password'] = '1234'
        request.POST['phone_number'] = '123456789'
        request._messages = messages.storage.default_storage(request)
        response = register_customer(request)
        assert(response.status_code, 302)

    def test_register_customer_null_username(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['username'] = ''
        request.POST['password'] = '12345'
        request.POST['re_password'] = '12345'
        request.POST['phone_number'] = '123456789'
        request._messages = messages.storage.default_storage(request)
        response = register_customer(request)
        assert(response.status_code, 302)

    def test_register_customer_null_password(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['username'] = 'mradulagrawal'
        request.POST['password'] = ''
        request.POST['re_password'] = ''
        request.POST['phone_number'] = '123456789'
        request._messages = messages.storage.default_storage(request)
        response = register_customer(request)
        assert(response.status_code, 302)

    def test_register_customer_reregister(self):
        self.test_register_customer_success()
        request = HttpRequest()
        request.method = 'POST'
        request.POST['username'] = 'mradulagrawal'
        request.POST['password'] = '12345'
        request.POST['re_password'] = '12345'
        request.POST['phone_number'] = '123456789'
        request._messages = messages.storage.default_storage(request)
        response = register_customer(request)
        assert(response.status_code, 302)