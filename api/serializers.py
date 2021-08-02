from rest_framework import serializers


class HotelsSerializer(serializers.Serializer):
    hotel_name = serializers.CharField(max_length=200)
    hotel_email = serializers.EmailField(max_length=254)
    hotel_url = serializers.URLField()


class RoomsSerializer(serializers.Serializer):
    room_number = serializers.IntegerField()
    room_rate_price = serializers.DecimalField(max_digits=7, decimal_places=2)

