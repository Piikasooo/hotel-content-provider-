from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django import forms
from hotelcontent.forms import AddHotelForm
from hotelcontent.views import AddHotelView
from hotelcontent.models import Hotel, Admin, RoomTypes, Amenity, Rooms
from unittest.mock import Mock, patch


class TestView(TestCase):

    def test_view_true(self):
        self.assertTrue(1)
