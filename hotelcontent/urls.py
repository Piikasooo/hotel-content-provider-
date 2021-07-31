from .views import LoginView, RegistrationView, HomePageView, CreateRoom, AddHotelView, HotelDetailView, CreateAmenityView, CreateCoefficientView
from django.urls import path


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('homepage/', HomePageView.as_view(), name='homepage'),
    path('add_hotel/', AddHotelView.as_view(), name='add_hotel'),

    path('rooms/<slug:slug>/', CreateRoom.as_view(), name='rooms'),
    path('amenities/<slug:slug>/', CreateAmenityView.as_view(), name='amenities'),
    path('coefficient/<slug:slug>/', CreateCoefficientView.as_view(), name='coefficient'),

    path('<slug:slug>/', HotelDetailView.as_view(), name="hotel_detail")
]