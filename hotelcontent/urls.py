from django.conf.urls import url

from .views import LoginView, RegistrationView, HomePageView, AddRoomView, AddHotelView, RoomsView, DetailsView
from django.urls import path


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('hotels/', HomePageView.as_view(), name='homepage'),
    path('add_room/', AddRoomView.as_view(), name='add_room'),
    path('add_hotel/', AddHotelView.as_view(), name='add_hotel'),
    path('hotels/<str:hotel_name>/rooms/', RoomsView.as_view(), name='rooms'),
    path('hotels/<str:hotel_name>/', DetailsView.as_view(), name='details')
    #url(r'^hotels/(?P<hotel_name>\w{0,50})/$', DetailsView.as_view(), name='details')
]