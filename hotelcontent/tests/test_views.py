from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from hotelcontent.models import Hotel, Admin, RoomTypes, Amenity, Rooms
import json


class TestView(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.credentials = {
            'username': 'tst',
            'password': 'QazxsW1234'}
        admin = User.objects.create_user(**self.credentials)
        Admin.objects.create(user=admin)

        hotel = Hotel.objects.create(
            hotel_name='setup_hotel',
            hotel_long=3.000012,
            hotel_lat=3.000103,
            hotel_email='setuptest@gmail.ua',
            hotel_url='http://www.testhotelurlsetup.net',
            hotel_description='some words',
            admin=admin,
            url='setup_hotelHotel'
        )

        RoomTypes.objects.create(
            room_type_name='room_type',
            room_type_price=100,
            room_type_description='description@gmail.ua',
            hotel=hotel,
        )

        Amenity.objects.create(
            amenity_name='test_amenity_2',
            amenity_price=200,
            hotel=hotel,
        )
        self.client.post(reverse('login'), {
            'username': 'tst',
            'password': 'QazxsW1234',
        })

    def assert_GET_method(self, url_name, html_name, args=None):
        response = self.client.get(reverse(url_name, args=args))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, html_name)

    def test_registration_GET(self):
        self.client.logout()
        self.assert_GET_method('registration', 'registration.html')

    def test_registration_POST(self):
        self.client.logout()
        response = self.client.post(reverse('registration'), {
            'username': 'django_test',
            'email': 'djangoemail@gmail.ua',
            'first_name': 'django_test_first_name',
            'last_name': 'django_test_last_name',
            'password': 'QazxsW1234',
            'confirm_password': 'QazxsW1234'
        })
        self.assertEquals(response.status_code, 302)
        user = User.objects.get(username='django_test')
        self.assertTrue(Admin.objects.filter(user=user).exists())

    def test_login_GET(self):
        self.client.logout()
        self.assert_GET_method('login', 'login.html')

    def test_login_POST(self):
        self.client.logout()
        response = self.client.post(reverse('login'), {
            'username': 'tst',
            'password': 'QazxsW1234',
        })
        self.assertEquals(response.status_code, 302)

    def test_homepage_GET(self):
        self.assert_GET_method('homepage', 'hotels.html')

    def test_add_hotel_GET(self):
        self.assert_GET_method('add_hotel', 'add_hotel.html')

    def test_add_hotel_POST(self):
        response = self.client.post(reverse('add_hotel'), {
            'hotel_name': 'hotel_test',
            'hotel_long': '3.000002',
            'hotel_lat': '3.000003',
            'hotel_email': 'emailfortest@gmail.ua',
            'hotel_url': 'http://www.testhotelurl.net',
            'hotel_description': 'some words',
        })
        self.assertEquals(response.status_code, 302)
        self.assertTrue(Hotel.objects.filter(hotel_name='hotel_test').exists())

    def test_rooms_GET(self):
        self.assert_GET_method('rooms', 'rooms.html', ['setup_hotelHotel'])

    def test_add_room_type_GET(self):
        self.assert_GET_method('add_room_type', 'add_room_type.html', ['setup_hotelHotel'])

    def test_add_room_type_POST(self):
        hotel = Hotel.objects.get(hotel_name='setup_hotel')
        response = self.client.post(reverse('add_room_type', args=['setup_hotelHotel']), {
            'room_type_name': 'test_room_type',
            'room_type_description': 'description',
            'room_type_price': 100,
            'hotel': hotel,
        })
        self.assertEquals(response.status_code, 302)
        self.assertTrue(RoomTypes.objects.filter(room_type_name='test_room_type').exists())

    def test_amenity_GET(self):
        self.assert_GET_method('amenity', 'createamenity.html', ['setup_hotelHotel'])

    def test_amenity_POST(self):
        hotel = Hotel.objects.get(hotel_name='setup_hotel')
        response = self.client.post(reverse('amenity', args=['setup_hotelHotel']), {
            'amenity_name': 'test_amenity',
            'amenity_price': 200,
            'hotel': hotel,
        })
        self.assertEquals(response.status_code, 302)
        self.assertTrue(Amenity.objects.filter(amenity_name='test_amenity').exists())

    def test_add_room_GET(self):
        self.assert_GET_method('add_room', 'createroom.html', ['setup_hotelHotel'])

    def test_add_room_POST(self):
        self.assertFalse(Rooms.objects.filter(room_number=1).exists())

        hotel = Hotel.objects.get(hotel_name='setup_hotel')
        room_type = RoomTypes.objects.get(room_type_name='room_type')
        amenity = Amenity.objects.get(amenity_name='test_amenity_2')
        response = self.client.post(reverse('add_room', args=['setup_hotelHotel']), {
            'dropdown': room_type,
            'room_number': 1,
            'hotel': hotel,
            'amenity': [amenity]

        })
        self.assertEquals(response.status_code, 302)
        self.assertTrue(Rooms.objects.filter(room_number=1).exists())
