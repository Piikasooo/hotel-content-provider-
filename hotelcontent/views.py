from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from .forms import LoginForm, RegistrationForm, DeleteForm, CreateCoefficientForm, AddHotelForm, CreateAmenityForm
from django.contrib.auth import authenticate, login
from .models import Admin, Hotel, Amenity, RoomTypes, Rooms, RateAmenity, Coefficient
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import CreateAmenityForm, CreateRoomForm, LoginForm, RegistrationForm, DeleteForm, AddHotelForm, \
    AddRoomTypeForm
from .models import Admin, Hotel, Amenity, RoomTypes, Rooms, RateAmenity
from .models import Admin, Hotel, Rooms


class LoginView(View):

    def get(self, request, *args, **kwargs):

        try:
            del request.session['data']
            form = LoginForm(request.POST or None)
            context = {'form': form}
            return render(request, 'login.html', context)
        except KeyError:
            form = LoginForm(request.POST or None)
            context = {'form': form}
            return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                request.session['data'] = user.username
                return HttpResponseRedirect('/homepage/')
        return render(request, 'login.html', {'form': form})


class RegistrationView(View):

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {'form': form}
        return render(request, 'registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Admin.objects.create(
                user=new_user,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
            )
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/login/')
        context = {'form': form}
        return render(request, 'registration.html', context)


class HomePageView(View):

    def get(self, request):

        form = DeleteForm(request.POST or None)

        user = request.user

        hotels = Hotel.objects.filter(admin=user)
        context = {
            'user': user,
            'hotels': hotels,
            'form': form
        }
        return render(request, "hotels.html", context)

    def post(self, request, *args, **kwargs):
        pass


class CreateRoom(View):

    def get(self, request, slug):

        user = request.user

        hotel = Hotel.objects.get(admin=user, url=slug)
        amenities = Amenity.objects.filter(hotel=hotel)
        room_types = RoomTypes.objects.filter(hotel=hotel)

        context = {'hotel': hotel, 'user': user, 'amenities': amenities, 'room_types': room_types}
        return render(request, "createroom.html", context)

    def post(self, request, slug):

        user = request.user

        amenities = request.POST.getlist('amenity')
        hotel = Hotel.objects.get(admin=user, url=slug)

        if len(amenities) == 0:
            amenities = Amenity.objects.filter(hotel=hotel)
            room_types = RoomTypes.objects.filter(hotel=hotel)
            context = {'hotel': hotel, 'user': user, 'amenities': amenities, 'room_types': room_types}
            alert = 'Select amenity'
            messages.info(request, alert)
            return render(request, "createroom.html", context)

        total = 0
        for amenity in amenities:
            amenity_name = amenity.split('/')[0]
            am = Amenity.objects.get(hotel=hotel, amenity_name=amenity_name)
            total = total + am.amenity_price

        room_number = request.POST.get('room_number')
        allrooms = Rooms.objects.filter(hotel=hotel)

        for roomhotel in allrooms:
            if roomhotel.room_number == int(room_number):
                amenities = Amenity.objects.filter(hotel=hotel)
                room_types = RoomTypes.objects.filter(hotel=hotel)
                context = {'hotel': hotel, 'user': user, 'amenities': amenities, 'room_types': room_types}
                alert = 'This number room exist!'
                messages.info(request, alert)
                return render(request, "createroom.html", context)

        room_type = request.POST.get('dropdown')
        if str(room_type) == 'Select type room':
            amenities = Amenity.objects.filter(hotel=hotel)
            room_types = RoomTypes.objects.filter(hotel=hotel)
            context = {'hotel': hotel, 'user': user, 'amenities': amenities, 'room_types': room_types}
            alert = 'Select type room'
            messages.info(request, alert)
            return render(request, "createroom.html", context)
        room_type_name = room_type.split('/')[0]
        room_type = RoomTypes.objects.get(room_type_name=room_type_name, hotel=hotel)

        room_rate_price = room_type.room_type_price + total
        room = Rooms(room_number=room_number, room_type=room_type, hotel=hotel, room_rate_price=room_rate_price)
        room.save()

        for amenity in amenities:
            amenity_name = amenity.split('/')[0]
            am = Amenity.objects.get(hotel=hotel, amenity_name=amenity_name)
            rate_amenity = RateAmenity(room=room, amenity=am)
            rate_amenity.save()
        alert = 'Successfully created new room'
        messages.info(request, alert)
        return HttpResponseRedirect('/homepage/')


class AddHotelView(View):

    @classmethod
    def _create_hotel(cls, form, user):
        if form.is_valid():
            new_hotel = form.save(commit=False)
            new_hotel.hotel_name = form.cleaned_data['hotel_name']
            new_hotel.hotel_long = form.cleaned_data['hotel_long']
            new_hotel.hotel_lat = form.cleaned_data['hotel_lat']
            new_hotel.hotel_email = form.cleaned_data['hotel_email']
            new_hotel.hotel_url = form.cleaned_data['hotel_url']
            new_hotel.admin = user
            new_hotel.hotel_description = form.cleaned_data['hotel_description']

            hotelname = form.cleaned_data['hotel_name']
            hotelname = hotelname.split()
            hotelname = ''.join(hotelname)

            url = hotelname + 'Hotel'
            new_hotel.url = url
            new_hotel.save()

            return new_hotel

    def get(self, request, *args, **kwargs):
        form = AddHotelForm(request.POST or None)
        context = {'form': form}
        return render(request, 'add_hotel.html', context)

    def post(self, request, *args, **kwargs):
        form = AddHotelForm(request.POST or None)
        user = request.user
        if self._create_hotel(form, user):
            return HttpResponseRedirect('/homepage/')
        context = {'form': form}
        return render(request, 'add_hotel.html', context)


class HotelDetailView(View):

    def get(self, request, slug):
        hotel = Hotel.objects.get(url=slug)
        amenities = Amenity.objects.filter(hotel=hotel)
        context = {"hotel": hotel, "amenities": amenities}
        return render(request, "hotel_detail.html", context)

    def post(self, request, slug):
        hotel = Hotel.objects.get(url=slug)
        hotel.delete()
        alert = 'Hotel is deleted'
        messages.info(request, alert)
        return HttpResponseRedirect('/homepage/')


class CreateAmenityView(View):

    def get(self, request, slug):

        form = CreateAmenityForm(request.POST or None)

        user = request.user

        hotel = Hotel.objects.get(url=slug, admin=user)

        amenities = Amenity.objects.filter(hotel=hotel)
        context = {'user': user, 'hotel': hotel, 'form': form, 'amenities': amenities}
        return render(request, "createamenity.html", context)

    def post(self, request, slug):

        form = CreateAmenityForm(request.POST or None)
        user = request.user

        if form.is_valid():

            hotel = Hotel.objects.get(url=slug, admin=user)

            amenity = form.save(commit=False)

            amenity_name = form.cleaned_data['amenity_name']

            if Amenity.objects.filter(hotel=hotel, amenity_name=amenity_name).exists():
                amenities = Amenity.objects.filter(hotel=hotel)
                context = {'user': user, 'hotel': hotel, 'form': form, 'amenities': amenities}
                alert = 'This amenity name exist'
                messages.info(request, alert)
                return render(request, "createamenity.html", context)

            amenity.amenity_name = amenity_name
            amenity.amenity_price = form.cleaned_data['amenity_price']
            amenity.hotel = hotel
            amenity.save()

            alert = 'Successfully created new amenity'
            messages.info(request, alert)
            return HttpResponseRedirect('/amenity/' + hotel.url + '/')
        hotel = Hotel.objects.get(url=slug)
        context = {'user': user, 'hotel': hotel, 'form': form}
        return render(request, "createamenity.html", context)


class CreateCoefficientView(View):

    def get(self, request, slug):
        form = CreateCoefficientForm(request.POST or None)
        user = request.user

        hotel = Hotel.objects.get(url=slug, admin=user)

        coefficients = Coefficient.objects.filter(hotel=hotel)
        context = {'user': user, 'hotel': hotel, 'form': form, 'coefficients': coefficients}
        return render(request, "coefficient.html", context)

    def post(self, request, slug):
        form = CreateCoefficientForm(request.POST or None)
        user = request.user

        hotel = Hotel.objects.get(url=slug, admin=user)

        if form.is_valid():
            coefficient = form.save(commit=False)
            coefficient.start_date = form.cleaned_data['start_date']
            coefficient.end_date = form.cleaned_data['end_date']
            coefficient.coefficient = form.cleaned_data['coefficient']
            coefficient.hotel = hotel
            coefficient.save()

            alert = 'Successfully created new coefficient'
            messages.info(request, alert)
            return HttpResponseRedirect('/coefficient/' + hotel.url + '/')
        context = {'user': user, 'hotel': hotel, 'form': form}
        return render(request, "coefficient.html", context)


class RoomsView(View):

    def get(self, request, slug):
        user = request.user
        hotel = Hotel.objects.get(url=slug)
        rooms = Rooms.objects.filter(hotel=hotel)
        context = {
            'user': user,
            'rooms': rooms,
            'hotel': hotel
        }
        return render(request, "rooms.html", context)


class AddRoomTypeView(View):

    def get(self, request, slug):
        form = AddRoomTypeForm(request.POST or None)

        user = request.user

        hotel = Hotel.objects.get(url=slug)
        room_type = RoomTypes.objects.filter(hotel=hotel)
        context = {
            'user': user,
            'hotel': hotel,
            'form': form,
            'room_type': room_type
        }
        return render(request, "add_room_type.html", context)

    def post(self, request, slug):
        form = AddRoomTypeForm(request.POST or None)
        user = request.user

        if form.is_valid():
            hotel = Hotel.objects.get(url=slug, admin=user)

            room_type = form.save(commit=False)
            room_type.room_type_name = form.cleaned_data['room_type_name']
            room_type.room_type_description = form.cleaned_data['room_type_description']
            room_type.room_type_price = form.cleaned_data['room_type_price']
            room_type.hotel = hotel
            room_type.save()

            return HttpResponseRedirect('/add_room_type/' + hotel.url + '/')
        hotel = Hotel.objects.get(url=slug)
        room_type = RoomTypes.objects.filter(hotel=hotel)
        context = {'user': user, 'hotel': hotel, 'form': form, 'room_type': room_type}
        return render(request, "add_room_type.html", context)


class RoomDetailView(View):

    def get(self, request, slug, room_number):
        hotel = Hotel.objects.get(url=slug)
        room = Rooms.objects.get(hotel=hotel, room_number=room_number)
        room_type = RoomTypes.objects.get(id=room.room_type.id)
        amenities = RateAmenity.objects.filter(room=room)
        context = {
            "hotel": hotel,
            "room": room,
            "room_type": room_type,
            "amenities": amenities,
        }
        return render(request, "room_details.html", context)