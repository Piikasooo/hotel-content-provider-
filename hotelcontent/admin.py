from django.contrib import admin
from .models import Admin, Hotel, Rooms, Room_types, Agent_reservation, Bookings, Booking_status


admin.site.register(Admin)
admin.site.register(Hotel)
admin.site.register(Rooms)
admin.site.register(Room_types)
admin.site.register(Agent_reservation)
admin.site.register(Bookings)
admin.site.register(Booking_status)