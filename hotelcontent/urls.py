from .views import LoginView, RegistrationView, HomePageView, AddHotelView
from django.urls import path
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('homepage/', HomePageView.as_view(), name='homepage'),
    path('add_hotel/', AddHotelView.as_view(), name='add_hotel'),

]