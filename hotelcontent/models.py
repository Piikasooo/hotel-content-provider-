from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Admin(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)

    # url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.user


class Hotel(models.Model):
    hotel_name = models.CharField(max_length=200)
    hotel_long = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    hotel_lat = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    hotel_email = models.EmailField(max_length=254)
    hotel_url = models.URLField()
    admin = models.ForeignKey(User, verbose_name="Администратор", on_delete=models.CASCADE, default=1)
    hotel_description = models.TextField(default='...')

    def __str__(self):
        return self.hotel_name

    '''def get_absolute_url(self):
        return reverse('hotels', kwargs={'hotel_name': self.hotel_name})
'''


class RoomTypes(models.Model):
    room_type_name = models.CharField(max_length=200)
    room_type_description = models.CharField(max_length=200)
    room_type_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.room_type_name


class Rooms(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomTypes, on_delete=models.CASCADE)
    room_number = models.IntegerField()

    def __str__(self):
        return str(self.room_number)


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


class Amenity(models.Model):
    amenity_name = models.CharField(max_length=200)
    amenity_price = models.DecimalField(max_digits=7, decimal_places=2)


class Coefficient(models.Model):
    start_date = models.DateField
    end_date = models.DateField
    coefficient = models.DecimalField(max_digits=7, decimal_places=2)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)


class RateAmenity(models.Model):
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    amenity = models.ManyToManyField(Amenity)

    def __str__(self):
        return '{}/{}'.format(self.room, self.amenity)
