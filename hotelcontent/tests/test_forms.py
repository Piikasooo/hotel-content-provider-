from django.contrib.auth.models import User
from django.test import TestCase, Client
from hotelcontent.forms import (
    AddHotelForm,
    AddRoomTypeForm,
    RegistrationForm,
    LoginForm,
    DeleteForm,
    CreateCoefficientForm,
    CreateAmenityForm,
)
from hotelcontent.models import Hotel, Admin, RoomTypes
from datetime import date, timedelta


class TestView(TestCase):

    def test_form_true(self):
        self.assertTrue(1)
