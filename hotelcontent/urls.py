from .views import LoginView, RegistrationView, HomePageView, CreateRoom, AddHotelView, HotelDetailView, \
    CreateAmenityView, RoomsView, AddRoomTypeView, RoomDetailView
from .views import LoginView, RegistrationView, HomePageView, CreateRoom, \
        AddHotelView, HotelDetailView, CreateAmenityView, \
        CreateCoefficientView, HotelUpdateView, AmenityUpdate, TypeRoomUpdate, CoefficientUpdate, RateUpdateView, \
    CreateAmenityView, RoomsView, AddRoomTypeView, RoomDetailView, AddHotelImage
from .views import LoginView, RegistrationView, HomePageView, CreateRoom, AddHotelView, \
    HotelDetailView, CreateAmenityView, CreateCoefficientView, HotelUpdateView
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
    path('rooms/<slug:slug>/<int:room_number>/', RoomDetailView.as_view(), name='room_detail'),
    path('<slug:slug>/', HotelDetailView.as_view(), name="hotel_detail"),
    path('UpdateInfo/<slug:slug>/', HotelUpdateView.as_view(), name='hotel_update'),
    path('amenity/<slug:slug>/<str:amenity_name>/', AmenityUpdate.as_view(), name='amenity_update'),
    path('room_type/<slug:slug>/<str:room_type_name>/', TypeRoomUpdate.as_view(), name='type_room_update'),
    path('coefficient_update/<slug:slug>/<int:id>/', CoefficientUpdate.as_view(), name='coef_update'),
    path('room/<slug:slug>/<int:room_number>/', RateUpdateView.as_view(), name='rate_update'),
    path('add_hotel_image/<slug:slug>/', AddHotelImage.as_view(), name='add_hotel_image'),

]