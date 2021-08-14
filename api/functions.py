from datetime import datetime
from hotelcontent.models import Hotel, Rooms, RateAmenity, Bookings, Coefficient, AgentReservation
import datetime
from .currency import convert_currency


def str_to_date(request):
    start_date = request.data.get("start_date")
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    start_date = start_date.date()

    end_date = request.data.get("end_date")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    end_date = end_date.date()
    return start_date, end_date


def final_price(room, start_date, end_date, request):
    st_date = start_date
    total_price = 0.00
    coefficients = Coefficient.objects.filter(hotel=Hotel.objects.get(hotel_name=room.hotel.hotel_name))

    for coefficient in coefficients:

        if (coefficient.start_date > end_date) | (coefficient.end_date < start_date):
            room.room_price = 0
            room.room_price = room.room_rate_price * int((end_date - start_date).days)
            room.room_price = convert_currency(room.room_price, request)
            room.save()
        else:
            room.room_price = 0
            while st_date != end_date:
                if coefficient.start_date <= st_date <= coefficient.end_date:
                    total_price = (float(room.room_rate_price) * float(coefficient.coefficient)) + total_price
                else:
                    total_price = total_price + float(room.room_rate_price)
                st_date = st_date + datetime.timedelta(days=1)
            room.room_price = total_price
            room.room_price = convert_currency(room.room_price, request)
            room.save()
    return room


def final_price_list(free_rooms, start_date, end_date, request):

    rooms = free_rooms
    free_rooms = []

    for room in rooms:
        room_append = final_price(room=room, start_date=start_date, end_date=end_date, request=request)
        free_rooms.append(room_append)
    return free_rooms



