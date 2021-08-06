from django.test import SimpleTestCase
from hotelcontent.views import LoginView, RegistrationView, \
    HomePageView, RoomsView, AddHotelView, HotelDetailView,\
    CreateAmenityView, CreateCoefficientView, RoomDetailView, \
    AddRoomTypeView, CreateRoom
from django.urls import reverse, resolve


class TestUrls(SimpleTestCase):

    def test_registration_url_resolves(self):
        url = reverse('registration')
        self.assertEquals(resolve(url).func.view_class, RegistrationView)

    def test_homepage_url_resolves(self):
        url = reverse('homepage')
        self.assertEquals(resolve(url).func.view_class, HomePageView)

    def test_add_hotel_url_resolves(self):
        url = reverse('add_hotel')
        self.assertEquals(resolve(url).func.view_class, AddHotelView)

    def test_rooms_url_resolves(self):
        url = reverse('rooms', args=['slug'])
        self.assertEquals(resolve(url).func.view_class, RoomsView)

    def test_add_room_types_url_resolves(self):
        url = reverse('add_room_type', args=['slug'])
        self.assertEquals(resolve(url).func.view_class, AddRoomTypeView)

    def test_create_room_resolves(self):
        url = reverse('add_room', args=['slug'])
        self.assertEquals(resolve(url).func.view_class, CreateRoom)

    def test_amenities_url_resolves(self):
        url = reverse('amenity', args=['slug'])
        self.assertEquals(resolve(url).func.view_class, CreateAmenityView)

    def test_coefficient_url_resolves(self):
        url = reverse('coefficient', args=['slug'])
        self.assertEquals(resolve(url).func.view_class, CreateCoefficientView)

    def test_hotel_detail_url_resolves(self):
        url = reverse('hotel_detail', args=['slug'])
        self.assertEquals(resolve(url).func.view_class, HotelDetailView)

    def test_room_detail_url_resolves(self):
        url = reverse('room_detail', args=['slug', 1])
        self.assertEquals(resolve(url).func.view_class, RoomDetailView)