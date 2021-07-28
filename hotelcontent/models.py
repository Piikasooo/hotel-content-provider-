from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Admin(models.Model):

    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)

    #url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.user


class Hotel(models.Model):
    hotel_name = models.CharField(max_length=200)

    hotel_long = models.DecimalField(max_digits=9, decimal_places=6)
    hotel_lat = models.DecimalField(max_digits=9, decimal_places=6)
    hotel_email = models.EmailField(max_length=254)
    hotel_url = models.URLField()
    admin = models.ForeignKey(User, verbose_name="Администратор", on_delete=models.CASCADE)

    hotel_description = models.TextField

    def __str__(self):
        return self.hotel_name


class Room_types(models.Model):
    hotel_type_name = models.CharField(max_length=200)
    hotel_type_description = models.CharField(max_length=200)
    hotel_type_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.hotel_type_name


class Rooms(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.ForeignKey(Room_types, on_delete=models.CASCADE)
    room_number = models.IntegerField()
    room_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.hotel, self.room_number, self.room_price


class Agent_reservation(models.Model):
    agent_details = models.CharField(max_length=200)

    def __str__(self):
        return self.agent_details


class Booking_status(models.Model):
    booking_status_description = models.CharField(max_length=200)

    def __str__(self):
        return self.booking_status_description


class Bookings(models.Model):
    agent_reservation = models.ForeignKey(Agent_reservation, on_delete=models.CASCADE)
    booking_status = models.ForeignKey(Booking_status, on_delete=models.CASCADE)
    hotels = models.ManyToManyField(Hotel)
    checkin = models.DateField()
    checkout = models.DateField(blank=True, null=True)
    rate_price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.agent_reservation, self.hotels, self.checkin, self.checkout


class Amenity(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)


class Coef(models.Model):
    start_date = models.DateField
    end_date = models.DateField
    coef = models.DecimalField(max_digits=7, decimal_places=2)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)


class Rate_Amenity(models.Model):
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    amenity = models.ManyToManyField(Amenity)