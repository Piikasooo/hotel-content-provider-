from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from hotelcontent.models import Hotel, Rooms, RateAmenity
from .serializers import HotelsSerializer, RoomSerializer


class HotelsView(generics.ListAPIView):

    serializer_class = HotelsSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        hotels = Hotel.objects.all()
        serializer = HotelsSerializer(hotels, many=True)
        return Response({"hotels": serializer.data})


class RoomsHotelView(APIView):
    permission_classes = [permissions.IsAuthenticated]

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