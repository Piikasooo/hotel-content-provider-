from rest_framework import serializers
from hotelcontent.models import Hotel, Rooms


class HotelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['hotel_name', 'hotel_email', 'hotel_url']


class RoomSerializer(serializers.ModelSerializer):
    hotel = serializers.CharField()
    room_type = serializers.CharField()
    amenities = serializers.StringRelatedField(many=True)

    class Meta:
        model = Rooms
        fields = ['hotel', 'room_number', 'room_type', 'room_rate_price', 'amenities']

