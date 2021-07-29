from django.contrib import admin
from .models import Admin, Hotel, Rooms, RoomTypes, AgentReservation, Bookings, BookingStatus, Coefficient, Amenity, RateAmenity


admin.site.register(Admin)
admin.site.register(Hotel)
admin.site.register(Rooms)
admin.site.register(RoomTypes)
admin.site.register(AgentReservation)
admin.site.register(Bookings)
admin.site.register(BookingStatus)
admin.site.register(Coefficient)
admin.site.register(Amenity)
admin.site.register(RateAmenity)
