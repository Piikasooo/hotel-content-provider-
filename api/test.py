import json

from rest_framework.test import APIRequestFactory
from django.test import TestCase, Client
from hotelcontent.models import Admin, Hotel, Rooms
from django.contrib.auth.models import User
from .serializers import HotelsSerializer
from rest_framework import status


class HotelsViewTest(TestCase):
    """ Test module for GET all hotels API """

    def setUp(self) -> None:
        self.client = Client()
        user = User.objects.create_user(username='test_api_user', password='QazxsW1234')
        admin = Admin.objects.create(user=user)
        first_hotel = Hotel.objects.create(
            hotel_name='test_api_first_hotel',
            hotel_long=1.00,
            hotel_lat=1.00,
            hotel_email='emailfortestapifirst@gmail.com',
            hotel_url='http://www.firsttesthotelurl.net',
            admin=user,
            hotel_description='some text',
            url='test_api_first_hotelHotel'
        )
        second_hotel = Hotel.objects.create(
            hotel_name='test_api_second_hotel',
            hotel_long=44.00,
            hotel_lat=44.00,
            hotel_email='emailfortestapisecond@gmail.com',
            hotel_url='http://www.secondtesthotelurl.net',
            admin=user,
            hotel_description='some text',
            url='test_api_second_hotelHotel'
        )

    def test_get_all_hotels_api(self):
        response = self.client.get('/api/v1/hotels/')
        hotels = Hotel.objects.all()
        serializer = HotelsSerializer(hotels, many=True)
        self.assertEqual(response.data["hotels"], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_hotels_area_api(self):
        valid_data = {
            'lat': 44,
            'long': 44,
        }
        response = self.client.post(f'/api/v1/hotels/',
                                    data=json.dumps(valid_data),
                                    content_type='application/json')
        hotels = Hotel.objects.filter(hotel_name='test_api_second_hotel')
        serializer = HotelsSerializer(hotels, many=True)
        self.assertEqual(response.data["hotels in range 10km"],
                         serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RoomsHotelViewTest(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        user = User.objects.create_user(username='test_api_user', password='QazxsW1234')
        admin = Admin.objects.create(user=user)
        first_hotel = Hotel.objects.create(
            hotel_name='test_api_first_hotel',
            hotel_long=1.00,
            hotel_lat=1.00,
            hotel_email='emailfortestapifirst@gmail.com',
            hotel_url='http://www.firsttesthotelurl.net',
            admin=user,
            hotel_description='some text',
            url='test_api_first_hotelHotel'
        )

        first_room_in_first_hotel =