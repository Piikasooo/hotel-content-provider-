from django.urls import path
from .views import HotelsView, RoomsFilterDateView, BookingView, MyBookingsView, CancelBooking

urlpatterns = [
    path('hotels/', HotelsView.as_view()),
    path('rates', RoomsFilterDateView.as_view()),
    path('booking', BookingView.as_view()),
    path('my_bookings/', MyBookingsView.as_view()),
    path('my_bookings/cancel', CancelBooking.as_view()),
]