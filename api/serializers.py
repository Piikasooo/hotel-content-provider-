from rest_framework import serializers
from hotelcontent.models import Hotel, Rooms, Bookings, HotelsImages


class HotelsSerializer(serializers.ModelSerializer):
    hotel = serializers.StringRelatedField(many=True)

    class Meta:
        model = Hotel
        fields = ['hotel_name', 'hotel_email', 'hotel_url', 'hotel_description', 'hotel_lat', 'hotel_long', 'hotel_image', 'hotel' ]


class RoomSerializer(serializers.ModelSerializer):
    hotel = serializers.CharField()
    room_type = serializers.CharField()
    amenities = serializers.StringRelatedField(many=True)

    class Meta:
        model = Rooms
        fields = ['hotel', 'room_number', 'room_type', 'amenities']


class RoomFilterSerializer(serializers.ModelSerializer):
    hotel = serializers.CharField()
    room_type = serializers.CharField()
    amenities = serializers.StringRelatedField(many=True)

    class Meta:
        model = Rooms
        fields = ['hotel', 'room_number', 'room_type', 'amenities', 'room_price']


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bookings
        fields = ['id', 'booking_stat', 'hotel', 'room_number', 'checkin', 'checkout', 'rate_price']