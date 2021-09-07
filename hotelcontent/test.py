from django.test import SimpleTestCase, TestCase
from hotelcontent.views import (
    LoginView,
    RegistrationView,
    HomePageView,
    RoomsView,
    AddHotelView,
    HotelDetailView,
    CreateAmenityView,
    CreateCoefficientView,
    RoomDetailView,
    AddRoomTypeView,
    CreateRoom,
)
from django.urls import reverse, resolve
from unittest.mock import Mock, patch
from hotelcontent.models import Hotel


class TestView(TestCase):

    @patch('hotelcontent.views.AddHotelView._create_hotel')
    def test_add_hotel_POST(self, mock_create_hotel):
        data = {}
        mock_create_hotel.is_valid.return_value = True
        response = self.client.post(reverse('add_hotel'), data=data)
        self.assertEquals(response.status_code, 302)
        self.assertFalse(Hotel.objects.filter(hotel_name='hotel_test').exists())
        print(mock_create_hotel.call_args)


class TestUrls(SimpleTestCase):
    def equals_for_url(self, url_name, view, args=None):
        url = reverse(url_name, args=args)
        return self.assertEquals(resolve(url).func.view_class, view)

    def test_login_url_resolves(self):
        self.equals_for_url("login", LoginView)

    def test_registration_url_resolves(self):
        self.equals_for_url("registration", RegistrationView)

    def test_homepage_url_resolves(self):
        self.equals_for_url("homepage", HomePageView)

    def test_add_hotel_url_resolves(self):
        self.equals_for_url("add_hotel", AddHotelView)

    def test_rooms_url_resolves(self):
        self.equals_for_url("rooms", RoomsView, ["slug"])

    def test_add_room_types_url_resolves(self):
        self.equals_for_url("add_room_type", AddRoomTypeView, ["slug"])

    def test_create_room_resolves(self):
        self.equals_for_url("add_room", CreateRoom, ["slug"])

    def test_amenities_url_resolves(self):
        self.equals_for_url("amenity", CreateAmenityView, ["slug"])

    def test_coefficient_url_resolves(self):
        self.equals_for_url("coefficient", CreateCoefficientView, ["slug"])

    def test_hotel_detail_url_resolves(self):
        self.equals_for_url("hotel_detail", HotelDetailView, ["slug"])

    def test_room_detail_url_resolves(self):
        self.equals_for_url("room_detail", RoomDetailView, ["slug", 1])
