from datetime import datetime
from hotelcontent.models import Hotel, Rooms, RateAmenity, Bookings, Coefficient, AgentReservation
from .currency import convert_to
import datetime


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
            room.save()
    return room


def final_price_list(free_rooms, start_date, end_date, request):

    rooms = free_rooms
    free_rooms = []

    for room in rooms:
        st_date = start_date
        total_price = 0.00
        coefficients = Coefficient.objects.filter(hotel=Hotel.objects.get(hotel_name=room.hotel.hotel_name))

        for coefficient in coefficients:

            if (coefficient.start_date > end_date) | (coefficient.end_date < start_date):
                room.room_price = 0
                room.room_price = room.room_rate_price * int((end_date - start_date).days)
                room.save()
                free_rooms = currency(request=request, room=room, free_rooms=free_rooms)
            else:
                room.room_price = 0
                while st_date != end_date:
                    if coefficient.start_date <= st_date <= coefficient.end_date:
                        total_price = (float(room.room_rate_price) * float(coefficient.coefficient)) + total_price
                    else:
                        total_price = total_price + float(room.room_rate_price)
                    st_date = st_date + datetime.timedelta(days=1)
                room.room_price = total_price
                room.save()
                free_rooms = currency(request=request, room=room, free_rooms=free_rooms)
    return free_rooms


def currency(request, room, free_rooms):
    if not request.data.get("currency"):
        room.save()
        free_rooms.append(room)
        return free_rooms
    elif request.data.get("currency") == "USD":
        usd = convert_to(currency=request.data.get("currency"))
        usd = float(usd.replace(',', 'COMMA').replace('.', ',').replace('COMMA', '.'))
        room.room_price = float(room.room_price) * usd
        room.save()
        free_rooms.append(room)
        return free_rooms
    elif request.data.get("currency") == "EUR":
        eur = convert_to(currency=request.data.get("currency"))
        room.room_price = room.room_price * float(eur)
        room.save()
        free_rooms.append(room)
        return free_rooms
    else:
        return free_rooms
