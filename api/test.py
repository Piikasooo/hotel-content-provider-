import json

from rest_framework.test import APIRequestFactory
from django.test import TestCase, Client
from hotelcontent.models import Admin, Hotel, Rooms, RoomTypes
from django.contrib.auth.models import User
from .serializers import HotelsSerializer, RoomSerializer
from rest_framework import status, permissions


class HotelsViewTest(TestCase):
    """ Test module for GET hotels API """

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

        room_type_in_first_hotel = RoomTypes.objects.create(
            room_type_name='setup_room_type_name',
            room_type_description='setup description text',
            room_type_price=100,
            hotel=first_hotel
        )
        room_type_in_second_hotel = RoomTypes.objects.create(
            room_type_name='setup_room_type_name_2',
            room_type_description='setup description text',
            room_type_price=100,
            hotel=second_hotel
        )

        first_room_in_first_hotel = Rooms.objects.create(
            hotel=first_hotel,
            room_type=room_type_in_first_hotel,
            room_number=1,
            room_rate_price=100,

        )

        second_room_in_first_hotel = Rooms.objects.create(
            hotel=first_hotel,
            room_type=room_type_in_first_hotel,
            room_number=2,
            room_rate_price=200,
        )

        first_room_in_second_hotel = Rooms.objects.create(
            hotel=second_hotel,
            room_type=room_type_in_second_hotel,
            room_number=1,
            room_rate_price=100,
        )

    def test_get_two_room_from_first_hotel(self):
        response = self.client.get('/api/v1/rooms/test_api_first_hotelHotel/')
        hotel = Hotel.objects.get(hotel_name='test_api_first_hotel')
        rooms = Rooms.objects.filter(hotel=hotel)
        serializer = RoomSerializer(rooms, many=True)
        self.assertEqual(response.data["rooms"], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RoomsViewTest(TestCase):

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

        room_type_in_first_hotel = RoomTypes.objects.create(
            room_type_name='setup_room_type_name',
            room_type_description='setup description text',
            room_type_price=100,
            hotel=first_hotel
        )
        room_type_in_second_hotel = RoomTypes.objects.create(
            room_type_name='setup_room_type_name_2',
            room_type_description='setup description text',
            room_type_price=100,
            hotel=second_hotel
        )

        first_room_in_first_hotel = Rooms.objects.create(
            hotel=first_hotel,
            room_type=room_type_in_first_hotel,
            room_number=1,
            room_rate_price=100,

        )

        second_room_in_first_hotel = Rooms.objects.create(
            hotel=first_hotel,
            room_type=room_type_in_first_hotel,
            room_number=2,
            room_rate_price=200,
        )

        first_room_in_second_hotel = Rooms.objects.create(
            hotel=second_hotel,
            room_type=room_type_in_second_hotel,
            room_number=1,
            room_rate_price=100,
        )

    def test_get_all_room(self):
        response = self.client.get('/api/v1/rooms/')
        rooms = Rooms.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        self.assertEqual(response.data["rooms"], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BookingViewTest(TestCase):
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

        room_type_in_first_hotel = RoomTypes.objects.create(
            room_type_name='setup_room_type_name',
            room_type_description='setup description text',
            room_type_price=100,
            hotel=first_hotel
        )
        room_type_in_second_hotel = RoomTypes.objects.create(
            room_type_name='setup_room_type_name_2',
            room_type_description='setup description text',
            room_type_price=100,
            hotel=second_hotel
        )

        first_room_in_first_hotel = Rooms.objects.create(
            hotel=first_hotel,
            room_type=room_type_in_first_hotel,
            room_number=1,
            room_rate_price=100,

        )

        second_room_in_first_hotel = Rooms.objects.create(
            hotel=first_hotel,
            room_type=room_type_in_first_hotel,
            room_number=2,
            room_rate_price=200,
        )

        first_room_in_second_hotel = Rooms.objects.create(
            hotel=second_hotel,
            room_type=room_type_in_second_hotel,
            room_number=1,
            room_rate_price=100,
        )



    def test_booking(self):
        user = self.client.post('/auth/jwt/create', data={
            'username': 'test_api_user',
            'password': 'QazxsW1234'
        })
        user_token = user.data['access']
        response = self.client.get('/api/v1/booking')
        #print(response)
        #self.assertEqual(response.status_code, status.HTTP_200_OK)


class RoomsFilterDateViewTest(TestCase):
    pass