from rest_framework import serializers
from hotelcontent.models import Hotel, Rooms, Bookings


class HotelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['hotel_name', 'hotel_email', 'hotel_url', 'hotel_description']


class RoomSerializer(serializers.ModelSerializer):
    hotel = serializers.CharField()
    room_type = serializers.CharField()
    amenities = serializers.StringRelatedField(many=True)

    class Meta:
        model = Rooms
        fields = ['hotel', 'room_number', 'room_type', 'room_rate_price', 'amenities']


class RoomFilterSerializer(serializers.ModelSerializer):
    hotel = serializers.CharField()
    room_type = serializers.CharField()
    amenities = serializers.StringRelatedField(many=True)

    class Meta:
        model = Rooms
        fields = ['hotel', 'room_number', 'room_type', 'amenities', 'room_rate_price']


class BookingSerializer(serializers.ModelSerializer):
    booking_status = serializers.CharField()
    hotels = serializers.CharField()
    room = serializers.CharField()

    class Meta:
        model = Bookings
        fields = ['hotels', 'room', 'checkin', 'checkout', 'rate_price']