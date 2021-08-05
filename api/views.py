from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from hotelcontent.models import Hotel, Rooms, RateAmenity, Bookings, Coefficient, AgentReservation
from .serializers import HotelsSerializer, RoomSerializer, BookingSerializer
import datetime


class HotelsView(APIView):

    def get(self, request):
        hotels = Hotel.objects.all()
        serializer = HotelsSerializer(hotels, many=True)
        return Response({"hotels": serializer.data})


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

                #libre_rooms = final_price(libre_rooms=libre_rooms, start_date=start_date, end_date=end_date)

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
