from .views import LoginView, RegistrationView, HomePageView, CreateRoom, AddHotelView, HotelDetailView, CreateAmenityView, RoomsView, AddRoomTypeView
from .views import LoginView, RegistrationView, HomePageView, CreateRoom, AddHotelView, HotelDetailView, CreateAmenityView, CreateCoefficientView
from django.urls import path


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('homepage/', HomePageView.as_view(), name='homepage'),
    path('add_hotel/', AddHotelView.as_view(), name='add_hotel'),

    path('rooms/<slug:slug>/', RoomsView.as_view(), name='rooms'),
    path('add_room_type/<slug:slug>/', AddRoomTypeView.as_view(), name='add_room_type'),
    path('add_room/<slug:slug>/', CreateRoom.as_view(), name='add_room'),
    path('amenity/<slug:slug>/', CreateAmenityView.as_view(), name='amenity'),
    path('coefficient/<slug:slug>/', CreateCoefficientView.as_view(), name='coefficient'),

    path('<slug:slug>/', HotelDetailView.as_view(), name="hotel_detail")
]