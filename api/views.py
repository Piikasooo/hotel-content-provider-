from rest_framework.response import Response
from rest_framework.views import APIView
from hotelcontent.models import Hotel, Rooms
from .serializers import HotelsSerializer, RoomsSerializer


class HotelsView(APIView):

    def get(self, request):
        hotels = Hotel.objects.all()
        serializer = HotelsSerializer(hotels, many=True)
        return Response({"hotels": serializer.data})


class RoomsHotelView(APIView):

    def get(self, request, slug):
        hotel = Hotel.objects.get(url=slug)
        rooms = Rooms.objects.filter(hotel=hotel)
        serializer = RoomsSerializer(rooms, many=True)
        return Response({"hotels": serializer.data})


class RoomsView(APIView):

    def get(self, request):
        rooms = Rooms.objects.all()
        serializer = RoomsSerializer(rooms, many=True)
        return Response({"hotels": serializer.data})