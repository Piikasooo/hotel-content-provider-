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
    hotel_address = models.CharField(max_length=200)
    hotel_email = models.CharField(max_length=200)
    hotel_url = models.CharField(max_length=200)


class Room_types(models.Model):
    hotel_type_name = models.CharField(max_length=200)
    hotel_tupe_description = models.CharField(max_length=200)


class Rooms(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.ForeignKey(Room_types, on_delete=models.CASCADE)
    room_number = models.IntegerField()
    room_rate = models.DecimalField(max_digits=5, decimal_places=2)
    smoking_yn = models.BooleanField()


class Agent_reservation(models.Model):
    agent_details = models.CharField(max_length=200)


class Booking_status(models.Model):
    booking_status_description = models.CharField(max_length=200)


class Bookings(models.Model):
    agent_reservation = models.ForeignKey(Agent_reservation, on_delete=models.CASCADE)
    booking_status = models.ForeignKey(Booking_status, on_delete=models.CASCADE)
    hotels = models.ManyToManyField(Hotel)
    from_date = models.DateField()
    until_date = models.DateField(blank=True, null=True)