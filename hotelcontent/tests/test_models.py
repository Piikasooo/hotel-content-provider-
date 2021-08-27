from django.test import TestCase
from django.contrib.auth.models import User
from hotelcontent.models import Hotel, Admin


class TestModels(TestCase):
    def setUp(self):
        self.credentials = {"username": "tst", "password": "QazxsW1234"}
        admin = User.objects.create_user(**self.credentials)
        Admin.objects.create(user=admin)

        self.hotel = Hotel.objects.create(
            hotel_name="setup_hotel",
            hotel_long=3.000012,
            hotel_lat=3.000103,
            hotel_email="setuptest@gmail.ua",
            hotel_url="http://www.testhotelurlsetup.net",
            hotel_description="some words",
            admin=admin,
            url="setup_hotelHotel",
        )
