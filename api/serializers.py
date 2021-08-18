from rest_framework import serializers

from hotelcontent.models import Hotel, Rooms, Bookings


class HotelsSerializer(serializers.ModelSerializer):
    hotel = serializers.StringRelatedField(many=True)

    class Meta:
        model = Hotel
        fields = [
            "hotel_name",
            "hotel_email",
            "hotel_url",
            "hotel_description",
            "hotel_lat",
            "hotel_long",
            "hotel_image",
            "hotel",
        ]


class RateSerializer(serializers.ModelSerializer):
    hotel = serializers.CharField()
    room_type = serializers.CharField()
    amenities = serializers.StringRelatedField(many=True)

    class Meta:
        model = Rooms
        fields = ["hotel", "room_number", "room_type", "amenities", "room_price"]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = [
            "id",
            "booking_stat",
            "hotel",
            "room_number",
            "checkin",
            "checkout",
            "rate_price",
        ]


class FilterHotelsSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    radius = serializers.FloatField()


class CancelBookingSerializer(serializers.Serializer):
    booking_id = serializers.IntegerField()


class CreateBookingSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    room_number = serializers.IntegerField()
    hotel = serializers.CharField()


class RateFilterSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    currency = serializers.CharField()
