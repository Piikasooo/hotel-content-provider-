import json
from rest_framework.test import APIRequestFactory
from django.test import TestCase, Client
from hotelcontent.models import (
    Admin,
    Hotel,
    Rooms,
    RoomTypes,
    AgentReservation,
    Bookings,
)
from django.contrib.auth.models import User
from .serializers import HotelsSerializer, BookingSerializer
from rest_framework import status, permissions
from datetime import date, timedelta


class HotelsViewTest(TestCase):
    """Test module for GET hotels API"""

    def test_true(self):
        self.assertTrue(1)

