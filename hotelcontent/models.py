from datetime import date

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Admin(models.Model):

    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)

    def __str__(self):
        return self.user


class Hotel(models.Model):
    hotel_name = models.CharField(max_length=200)
    hotel_long = models.DecimalField(max_digits=9, decimal_places=6)
    hotel_lat = models.DecimalField(max_digits=9, decimal_places=6)
    hotel_email = models.EmailField(max_length=254)
    hotel_url = models.URLField()

    admin = models.ForeignKey(User, verbose_name="Администратор", on_delete=models.CASCADE)
    hotel_description = models.TextField(default='Описание отеля')

    #url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.hotel_name


class RoomTypes(models.Model):
    room_type_name = models.CharField(max_length=200)
    room_type_description = models.CharField(max_length=200)
    room_type_price = models.DecimalField(max_digits=6, decimal_places=2, default=300)

    def __str__(self):
        return '{}/{}'.format(self.room_type_name, self.room_type_price)


class Amenity(models.Model):
    amenity_name = models.CharField(max_length=200)
    amenity_price = models.DecimalField(max_digits=7, decimal_places=2, default=50)

    def __str__(self):
        return '{}/{}'.format(self.amenity_name, self.amenity_price)


class Rooms(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomTypes, on_delete=models.CASCADE)
    room_number = models.IntegerField()

    def __str__(self):
        return '{}/{}'.format(self.hotel, self.room_number, self.room_type)


class AgentReservation(models.Model):
    agent_details = models.CharField(max_length=200)

    def __str__(self):
        return self.agent_details


class BookingStatus(models.Model):
    booking_status_description = models.CharField(max_length=200)

    def __str__(self):
        return self.booking_status_description


class Bookings(models.Model):
    agent_reservation = models.ForeignKey(AgentReservation, on_delete=models.CASCADE)
    booking_status = models.ForeignKey(BookingStatus, on_delete=models.CASCADE)
    hotels = models.ManyToManyField(Hotel)
    checkin = models.DateField()
    checkout = models.DateField(blank=True, null=True)
    rate_price = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    def __str__(self):
        return '{}/{}'.format(self.agent_reservation, self.hotels, self.checkin, self.checkout, self.rate_price)


class Coef(models.Model):
    start_date = models.DateField(default=date.today())
    end_date = models.DateField(default=date.today())
    coef = models.DecimalField(max_digits=7, decimal_places=2, default=1.1)
    hotel = models.ForeignKey(Hotel, verbose_name="Отель", on_delete=models.CASCADE)

    def __str__(self):
        return '{}/{}'.format(self.coef, self.start_date, self.end_date)


class RateAmenity(models.Model):
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    amenity = models.ManyToManyField(Amenity)

    def __str__(self):
        return '{}/{}'.format(self.room, self.amenity)