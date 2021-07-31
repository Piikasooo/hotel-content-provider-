from .views import LoginView, RegistrationView, HomePageView, CreateRoom, AddHotelView, HotelDetailView, CreateAmenityView
from django.urls import path


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('homepage/', HomePageView.as_view(), name='homepage'),
    path('add_hotel/', AddHotelView.as_view(), name='add_hotel'),

    path('createroom/<slug:slug>/', CreateRoom.as_view(), name='createroom'),
    path('createamenity/<slug:slug>/', CreateAmenityView.as_view(), name='createamenity'),

    path('<slug:slug>/', HotelDetailView.as_view(), name="hotel_detail")
]