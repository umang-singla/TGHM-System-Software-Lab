from django.test import TestCase
from manager.models import Admin, Station, Train

class AdminTestCase(TestCase):
    def setUp(self) -> None:
        Admin.objects.create(username="Mradul Agrawal")