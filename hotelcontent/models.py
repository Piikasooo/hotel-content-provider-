from datetime import date

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class Admin(models.Model):

    user = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.CASCADE
    )
    phone = models.CharField(
        max_length=20, verbose_name="Номер телефона", null=True, blank=True
    )
    address = models.CharField(
        max_length=255, verbose_name="Адрес", null=True, blank=True
    )

    def __str__(self):
        return "{}".format(self.user)


class Hotel(models.Model):
    hotel_name = models.CharField(max_length=200)
    hotel_long = models.DecimalField(max_digits=9, decimal_places=6)
    hotel_lat = models.DecimalField(max_digits=9, decimal_places=6)
    hotel_email = models.EmailField(max_length=254)
    hotel_url = models.URLField()
    hotel_image = models.ImageField(upload_to="hotels", null=True, blank=True)
    admin = models.ForeignKey(
        User, verbose_name="Администратор", on_delete=models.CASCADE
    )
    hotel_description = models.TextField(default="Описание отеля")

    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.hotel_name

    def get_absolute_url(self):
        return reverse("hotel_detail", kwargs={"slug": self.url})


class RoomTypes(models.Model):
    room_type_name = models.CharField(max_length=200)
    room_type_description = models.CharField(max_length=200)
    room_type_price = models.DecimalField(max_digits=6, decimal_places=2, default=300)

    hotel = models.ForeignKey(
        Hotel, verbose_name="Отель", on_delete=models.CASCADE, default=0
    )

    def __str__(self):
        return "{}".format(self.room_type_name)


class Amenity(models.Model):
    amenity_name = models.CharField(max_length=200)
    amenity_price = models.DecimalField(max_digits=7, decimal_places=2)

    hotel = models.ForeignKey(
        Hotel, verbose_name="Отель", on_delete=models.CASCADE, default=0
    )

    def __str__(self):
        return "{}".format(self.amenity_name)


class Rooms(models.Model):

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomTypes, on_delete=models.CASCADE)
    room_number = models.IntegerField()
    room_rate_price = models.DecimalField(
        max_digits=7, decimal_places=2, default=200.00
    )
    room_price = models.DecimalField(
        max_digits=7, decimal_places=2, default=200.00, blank=True
    )

    def __str__(self):
        return "{}/{}".format(
            self.hotel, self.room_number, self.room_type, self.room_rate_price
        )


class AgentReservation(models.Model):
    agent = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.CASCADE
    )

    def __str__(self):
        return "{}".format(self.agent)


class Bookings(models.Model):
    agent_reservation = models.ForeignKey(AgentReservation, on_delete=models.CASCADE)
    booking_stat = models.BooleanField(default=False)
    hotels = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True)
    checkin = models.DateField()
    checkout = models.DateField()
    rate_price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    room = models.ForeignKey(Rooms, on_delete=models.SET_NULL, null=True)

    # reserve field
    room_number = models.IntegerField(blank=True)
    hotel = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return "{}/{}".format(
            self.agent_reservation,
            self.hotels,
            self.room_number,
            self.checkin,
            self.checkout,
            self.rate_price,
        )


class Coefficient(models.Model):
    start_date = models.DateField(default=date.today())
    end_date = models.DateField(default=date.today())
    coefficient = models.DecimalField(max_digits=7, decimal_places=2, default=1.1)
    hotel = models.ForeignKey(Hotel, verbose_name="Отель", on_delete=models.CASCADE)

    def __str__(self):
        return "{}/{}".format(self.coefficient, self.start_date, self.end_date)


class RateAmenity(models.Model):
    room = models.ForeignKey(
        Rooms,
        related_name="amenities",
        verbose_name="Комната",
        on_delete=models.CASCADE,
        default=0,
    )
    amenity = models.ForeignKey(
        Amenity, verbose_name="Amenity", on_delete=models.CASCADE, default=0
    )

    def __str__(self):
        return "{}".format(self.amenity)


class HotelsImages(models.Model):
    hotel_photo = models.ImageField(null=True, upload_to="hotels")
    photo_description = models.CharField(blank=True, max_length=50)

    hotel = models.ForeignKey(Hotel, related_name="hotel", on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.hotel_photo, self.photo_description)
