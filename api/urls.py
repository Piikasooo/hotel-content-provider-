from django.urls import path
from .views import HotelsView, RoomsHotelView, RoomsView, RoomsFilterDateView, MyBookingsView

urlpatterns = [
    path('hotels/', HotelsView.as_view()),
    path('rooms/<slug:slug>/', RoomsHotelView.as_view()),
    path('rooms/', RoomsView.as_view()),
    path('rooms/FilterDate', RoomsFilterDateView.as_view()),
    path('my_bookings/<slug:slug>', MyBookingsView.as_view()),
]