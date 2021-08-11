from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from geopy.distance import great_circle
from hotelcontent.models import Hotel, Rooms, RateAmenity, Bookings, Coefficient, AgentReservation, User
from .serializers import HotelsSerializer, RoomSerializer, RoomFilterSerializer, BookingSerializer
from .functions import str_to_date, final_price_list, final_price
from django.db.models import Q
from rest_framework import permissions


class HotelsView(APIView):

    def get(self, request):
        hotels = Hotel.objects.all()
        serializer = HotelsSerializer(hotels, many=True)
        return Response({"hotels": serializer.data})

    def post(self, request):
        filter_hotels = []
        lat = float(request.data.get("lat"))
        long = float(request.data.get("long"))
        rad = float(request.data.get("rad"))

        # for hotel in hotels:
        #   fhotel_long = float(hotel.hotel_long)
        #   fhotel_lat = float(hotel.hotel_lat)
        #   if great_circle((fhotel_lat, fhotel_long), (lat, long)).kilometers <= 10:

        '''filter_hotels.append(Hotel.objects.raw('select * from hotelcontent_hotel where point(hotel_lat, '
                                               'hotel_long) <@> point(46.433495, 30.763270) <= 5'))
        '''

        for p in Hotel.objects.raw(
                'SELECT * FROM hotelcontent_hotel WHERE earth_distance(ll_to_earth(' + str(lat) + ', '
                + str(long) + '),ll_to_earth(float8(hotel_lat), float8(hotel_long))) / 1000 <= ' + str(rad)):
            filter_hotels.append(p)

        serializer = HotelsSerializer(filter_hotels, many=True)

        return Response({"hotels in range " + str(rad) + "km": serializer.data})


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


class CancelBooking(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response("Cancel your booking by id!")

    def post(self, request):
        # agent_name = request.user.username
        booking_id = request.data.get('id')
        booking = Bookings.objects.get(id=booking_id)
        booking.booking_stat = False
        booking.save()

        return Response('Successfully canceled', status=status.HTTP_200_OK)


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


class BookingView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response("Create new Booking!")

    def post(self, request):
        agent_name = request.user.username
        agent = User.objects.get(username=agent_name)
        agent1 = AgentReservation.objects.get(agent=agent)

        start_date, end_date = str_to_date(request)
        room_num = int(request.data.get("room_number"))
        hotel = Hotel.objects.get(hotel_name=request.data.get("hotel"))
        room = Rooms.objects.get(room_number=room_num, hotel=hotel)

        if not Rooms.objects.filter(
                Q(hotel=hotel), Q(room_number=room.room_number),
                Q(bookings__checkin__gt=end_date) | Q(bookings__checkout__lt=start_date)
        ).exists():
            return Response('Not created, Booking is exist', status=status.HTTP_400_BAD_REQUEST)

        room = final_price(room=room, start_date=start_date, end_date=end_date, request=request)

        booking = Bookings(agent_reservation=agent1,
                           booking_stat=True,
                           hotels=hotel,
                           checkin=start_date,
                           checkout=end_date,
                           rate_price=room.room_price,
                           room=room)
        booking.save()
        return Response('Successfully created', status=status.HTTP_201_CREATED)


class RoomsFilterDateView(APIView):

    def get(self, request):
        rooms = Rooms.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response({"rooms": serializer.data})

    def post(self, request):
        start_date, end_date = str_to_date(request)

        free_rooms = Rooms.objects.filter(
            Q(bookings=None) | (
                    Q(bookings__checkin__gt=end_date) | Q(bookings__checkout__lt=start_date))
        )
        free_rooms = final_price_list(free_rooms=free_rooms, start_date=start_date, end_date=end_date, request=request)
        serializer = RoomFilterSerializer(free_rooms, many=True)
        return Response({"rooms": serializer.data})


class MyBookingsView(APIView):

    def get(self, request):
        agent_name = request.user.username
        agent = User.objects.get(username=agent_name)
        agent1 = AgentReservation.objects.get(agent=agent)

        bookings = Bookings.objects.filter(agent_reservation=agent1)
        serializer = BookingSerializer(bookings, many=True)
        return Response({"Bookings": serializer.data})
