import math

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from hotelcontent.models import Hotel, Rooms, RateAmenity, Bookings, Coefficient, AgentReservation
from .serializers import HotelsSerializer, RoomSerializer, BookingSerializer
import datetime
from geopy.distance import great_circle


class HotelsView(APIView):

    def get(self, request):
        hotels = Hotel.objects.all()
        serializer = HotelsSerializer(hotels, many=True)
        return Response({"hotels": serializer.data})

    def post(self, request):
        filter_hotels = []
        lat = float(request.data.get("lat"))
        long = float(request.data.get("long"))

        hotels = Hotel.objects.all()

        for hotel in hotels:
            fhotel_long = float(hotel.hotel_long)
            fhotel_lat = float(hotel.hotel_lat)
            if great_circle((fhotel_lat, fhotel_long), (lat, long)).kilometers <= 100:
                # distance(fhotel_lat, fhotel_long, lat, long) <= 10:
                filter_hotels.append(hotel)

        serializer = HotelsSerializer(filter_hotels, many=True)

        return Response({"hotels in range 10km": serializer.data})

"""
def distance(hotel_lat, hotel_long, filter_lat, filter_long):

    # pi - число pi, rad - радиус сферы (Земли)
    rad = 6372795

    # в радианах
    lat1 = hotel_lat * math.pi / 180.
    lat2 = filter_lat * math.pi / 180.
    long1 = hotel_long * math.pi / 180.
    long2 = filter_long * math.pi / 180.

    # косинусы и синусы широт и разницы долгот
    cl1 = math.cos(lat1)
    cl2 = math.cos(lat2)
    sl1 = math.sin(lat1)
    sl2 = math.sin(lat2)
    delta = long2 - long1
    cdelta = math.cos(delta)
    sdelta = math.sin(delta)

    # вычисления длины большого круга
    y = math.sqrt(math.pow(cl2 * sdelta, 2) + math.pow(cl1 * sl2 - sl1 * cl2 * cdelta, 2))
    x = sl1 * sl2 + cl1 * cl2 * cdelta
    ad = math.atan2(y, x)
    dist = ad * rad

    return dist / 1000
"""


class RoomsHotelView(APIView):

    def get(self, request, slug):
        hotel = Hotel.objects.get(url=slug)
        rooms = Rooms.objects.filter(hotel=hotel)
        serializer = RoomSerializer(rooms, many=True)
        return Response({"rooms": serializer.data})


class RoomsView(APIView):

    def get(self, request):
        rooms = Rooms.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response({"rooms": serializer.data})


class RoomsFilterDateView(APIView):

    def get(self, request):
        rooms = Rooms.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response({"rooms": serializer.data})

    def post(self, request):

        start_date = request.data.get("start_date")
        end_date = request.data.get("end_date")

        rooms = Rooms.objects.all()
        libre_rooms = []
        for room in rooms:
            if not Bookings.objects.filter(room=room).exists():
                libre_rooms.append(room)
            else:
                checkroom = Bookings.objects.get(room=room)
                start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
                start_date = start_date.date()
                end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
                end_date = end_date.date()
                if not date_intersection((start_date, end_date), (checkroom.checkin, checkroom.checkout)):
                    libre_rooms.append(room)

                # libre_rooms = final_price(libre_rooms=libre_rooms, start_date=start_date, end_date=end_date)

        serializer = RoomSerializer(libre_rooms, many=True)
        return Response({"rooms": serializer.data})


def date_intersection(t1, t2):
    t1start, t1end = t1[0], t1[1]
    t2start, t2end = t2[0], t2[1]

    if t1end < t2start: return False
    if t1end == t2start: return True
    if t1start == t2start: return True
    if t1start < t2start and t2start < t1end: return True
    if t1start > t2start and t1end < t2end: return True
    if t1start < t2start and t1end > t2end: return True
    if t1start < t2end and t1end > t2end: return True
    if t1start > t2start and t1start < t2end: return True
    if t1start == t2end: return True
    if t1end == t2end: return True
    if t1start > t2end: return False


def final_price(libre_rooms, start_date, end_date):
    rooms = libre_rooms
    libre_rooms = []
    for room in rooms:
        hotel = Hotel.objects.get(hotel_name=room.hotel.hotel_name)

        coefficients = Coefficient.objects.filter(hotel=hotel)

        for coefficient in coefficients:

            if not date_intersection((start_date, end_date), (coefficient.start_date, coefficient.end_date)):
                room.room_rate_price = room.room_rate_price * int(abs((end_date - start_date).days))
                room.save()
                libre_rooms.append(room)
            else:
                pass

    return libre_rooms


class MyBookingsView(APIView):

    def get(self, request, slug):
        agent = AgentReservation.objects.filter(agent_details=slug).first()
        bookings = Bookings.objects.filter(agent_reservation=agent)
        serializer = BookingSerializer(bookings, many=True)
        return Response({"Bookings": serializer.data})
