import json
from rest_framework.test import APIRequestFactory
from django.test import TestCase, Client
from hotelcontent.models import Admin, Hotel, Rooms, RoomTypes, AgentReservation, Bookings
from django.contrib.auth.models import User
from .serializers import HotelsSerializer, RoomSerializer, BookingSerializer
from rest_framework import status, permissions
from datetime import date, timedelta


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
        agent = AgentReservation.objects.create(agent=user)
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

    def test_get_booking(self):
        user = self.client.post('/auth/jwt/create', data={
            'username': 'test_api_user',
            'password': 'QazxsW1234'
        })
        user_token = user.data['access']
        response = self.client.get('/api/v1/booking', HTTP_AUTHORIZATION=f'JWT {user_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_booking(self):
        user = self.client.post('/auth/jwt/create', data={
            'username': 'test_api_user',
            'password': 'QazxsW1234'
        })
        user_token = user.data['access']
        booking_data = {
            'start_date': '2021-09-11',
            'end_date': '2021-09-13',
            'hotel': 'test_api_first_hotel',
            'room_number': '1'
        }
        # normal data
        response = self.client.post('/api/v1/booking', data=booking_data, HTTP_AUTHORIZATION=f'JWT {user_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # exist booking
        response = self.client.post('/api/v1/booking', data=booking_data, HTTP_AUTHORIZATION=f'JWT {user_token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, 'Not created, Booking is exist')

        # boking room with booking_status=True
        booking_data['start_date'] = '2021-09-10'
        response = self.client.post('/api/v1/booking', data=booking_data, HTTP_AUTHORIZATION=f'JWT {user_token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, 'Not created, Booking is exist')

        # post with empty start_date field
        booking_data['start_date'] = ''
        response = self.client.post('/api/v1/booking', data=booking_data, HTTP_AUTHORIZATION=f'JWT {user_token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, 'start_date and end_date must be not Empty')

        # post with incorrect start_date field
        booking_data['start_date'] = '2021-08-10'
        response = self.client.post('/api/v1/booking', data=booking_data, HTTP_AUTHORIZATION=f'JWT {user_token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, 'Incorrect start_date or end_date')


class MyBookingsViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        first_user = User.objects.create_user(username='first_test_api_user', password='QazxsW1234')
        second_user = User.objects.create_user(username='second_test_api_user', password='QazxsW1234')
        first_admin = Admin.objects.create(user=first_user)
        second_admin = Admin.objects.create(user=second_user)
        second_agent = AgentReservation.objects.create(agent=second_user)
        first_agent = AgentReservation.objects.create(agent=first_user)
        first_hotel = Hotel.objects.create(
            hotel_name='test_api_first_hotel',
            hotel_long=1.00,
            hotel_lat=1.00,
            hotel_email='emailfortestapifirst@gmail.com',
            hotel_url='http://www.firsttesthotelurl.net',
            admin=first_user,
            hotel_description='some text',
            url='test_api_first_hotelHotel'
        )

        second_hotel = Hotel.objects.create(
            hotel_name='test_api_second_hotel',
            hotel_long=44.00,
            hotel_lat=44.00,
            hotel_email='emailfortestapisecond@gmail.com',
            hotel_url='http://www.secondtesthotelurl.net',
            admin=first_user,
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

        first_room_in_second_hotel = Rooms.objects.create(
            hotel=second_hotel,
            room_type=room_type_in_second_hotel,
            room_number=1,
            room_rate_price=100,
        )

    def test_get_my_booking(self):
        first_agent = self.client.post('/auth/jwt/create', data={
            'username': 'first_test_api_user',
            'password': 'QazxsW1234'
        })
        first_agent_token = first_agent.data['access']

        second_agent = self.client.post('/auth/jwt/create', data={
            'username': 'second_test_api_user',
            'password': 'QazxsW1234'
        })
        second_agent_token = second_agent.data['access']

        first_booking_data = {
            'start_date': '2021-09-11',
            'end_date': '2021-09-13',
            'hotel': 'test_api_first_hotel',
            'room_number': '1'
        }
        second_booking_data = {
            'start_date': '2021-09-11',
            'end_date': '2021-09-13',
            'hotel': 'test_api_second_hotel',
            'room_number': '1'
        }

        response = self.client.post('/api/v1/booking', data=first_booking_data,
                                    HTTP_AUTHORIZATION=f'JWT {first_agent_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post('/api/v1/booking', data=second_booking_data,
                                    HTTP_AUTHORIZATION=f'JWT {second_agent_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get('/api/v1/my_bookings/',
                                   HTTP_AUTHORIZATION=f'JWT {second_agent_token}')

        user = User.objects.get(username='second_test_api_user')
        agent = AgentReservation.objects.get(agent=user)
        bookings = Bookings.objects.filter(agent_reservation=agent)
        serializer = BookingSerializer(bookings, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["Bookings"], serializer.data)

