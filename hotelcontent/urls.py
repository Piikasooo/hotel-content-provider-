from .views import LoginView, RegistrationView, HomePageView, CreateRoom, AddHotelView
from django.urls import path


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('homepage/', HomePageView.as_view(), name='homepage'),
    path('createroom/', CreateRoom.as_view(), name='createroom'),
    path('add_hotel/', AddHotelView.as_view(), name='add_hotel'),
]