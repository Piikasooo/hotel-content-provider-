from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from hotelcontent.models import Hotel, Rooms, Bookings, AgentReservation, User
from .functions import str_to_date, final_price_list, final_price
from .serializers import (
    HotelsSerializer,
    RoomSerializer,
    RoomFilterSerializer,
    BookingSerializer,
    BodySerializer,
)


class HotelsView(APIView):
    """Endpoint for viewing available hotels"""

    # test_param1 = openapi.Parameter(
    #     "lat",
    #     openapi.IN_BODY,
    #     description="test manual param",
    #     type=openapi.TYPE_NUMBER,
    # )

    def get(self):
        hotels = Hotel.objects.all()
        serializer = HotelsSerializer(hotels, many=True)
        return Response({"hotels": serializer.data})

    @swagger_auto_schema(request_body=BodySerializer)
    def post(self, request):
        filter_hotels = []
        lat = float(request.data.get("lat"))
        long = float(request.data.get("long"))
        rad = float(request.data.get("rad"))

        for p in Hotel.objects.raw(
            "SELECT * FROM hotelcontent_hotel WHERE earth_distance(ll_to_earth({0},{1}),ll_to_earth(float8("
            "hotel_lat), float8(hotel_long))) / 1000 <= {2}".format(lat, long, rad)
        ):
            filter_hotels.append(p)

        serializer = HotelsSerializer(filter_hotels, many=True)

        return Response({"hotels in range " + str(rad) + "km": serializer.data})


class CancelBooking(APIView):
    """Endpoint for canceling active bookings"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self):
        return Response("Cancel your booking by id!")

    def post(self, request):
        user_name = request.user.username
        user = User.objects.get(username=user_name)
        agent = AgentReservation.objects.get(agent=user)
        booking_id = request.data.get("id")
        try:
            booking = Bookings.objects.get(id=booking_id, agent_reservation=agent)
            booking.booking_stat = False
            booking.save()
            return Response("This booking has been canceled", status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(
                "Error! Booking with this id doesn't exist!",
                status=status.HTTP_404_NOT_FOUND,
            )


class BookingView(APIView):
    """Endpoint for booking a rate"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self):
        return Response(
            "Required fields for create new booking: "
            "start_date, "
            "end_date, "
            "room_number, "
            "hotel"
        )

    def post(self, request):
        agent_name = request.user.username
        agent_user = User.objects.get(username=agent_name)
        agent = AgentReservation.objects.get(agent=agent_user)

        start_date, end_date = str_to_date(request)

        if start_date == "error":
            return Response(
                "start_date and end_date must be not Empty",
                status=status.HTTP_400_BAD_REQUEST,
            )
        if start_date == "incorrect date":
            return Response(
                "Incorrect start_date or end_date", status=status.HTTP_400_BAD_REQUEST
            )

        room_num = int(request.data.get("room_number"))
        hotel = Hotel.objects.get(hotel_name=request.data.get("hotel"))
        room = Rooms.objects.get(room_number=room_num, hotel=hotel)

        if Rooms.objects.filter(
            Q(id=room.id)
            & Q(bookings__booking_stat=True)
            & (
                (
                    Q(bookings__checkin__lt=end_date)
                    & Q(bookings__checkout__gte=end_date)
                )
                | (
                    Q(bookings__checkin__lte=start_date)
                    & Q(bookings__checkout__gt=start_date)
                )
            )
        ).exists():
            return Response(
                "Not created, Booking is exist", status=status.HTTP_400_BAD_REQUEST
            )

        room = final_price(
            room=room, start_date=start_date, end_date=end_date, request=request
        )

        booking = Bookings(
            agent_reservation=agent,
            booking_stat=True,
            hotels=hotel,
            checkin=start_date,
            checkout=end_date,
            rate_price=room.room_price,
            room=room,
            room_number=room.room_number,
            hotel=hotel.hotel_name,
        )
        booking.save()
        return Response("Successfully created", status=status.HTTP_201_CREATED)


class RoomsFilterDateView(APIView):
    """Endpoint for viewing available rates"""

    def get(self):
        rooms = Rooms.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response({"rooms": serializer.data})

    def post(self, request):
        start_date, end_date = str_to_date(request)

        free_rooms = list(
            Rooms.objects.exclude(
                Q(bookings__booking_stat=True)
                & (
                    (
                        Q(bookings__checkin__lt=end_date)
                        & Q(bookings__checkout__gte=end_date)
                    )
                    | (
                        Q(bookings__checkin__lte=start_date)
                        & Q(bookings__checkout__gt=start_date)
                    )
                )
            )
        )
        free_rooms = final_price_list(
            free_rooms=free_rooms,
            start_date=start_date,
            end_date=end_date,
            request=request,
        )
        serializer = RoomFilterSerializer(free_rooms, many=True)
        return Response({"rooms": serializer.data})


class MyBookingsView(APIView):
    """Endpoint for viewing available bookings"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        agent_name = request.user.username
        agent_object = User.objects.get(username=agent_name)
        agent = AgentReservation.objects.get(agent=agent_object)

        bookings = Bookings.objects.filter(agent_reservation=agent)
        serializer = BookingSerializer(bookings, many=True)
        return Response({"Bookings": serializer.data})
