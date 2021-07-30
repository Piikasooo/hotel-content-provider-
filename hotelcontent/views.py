from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from .forms import LoginForm, RegistrationForm, DeleteForm, AddHotelForm, CreateAmenityForm, CreateRoomForm
from django.contrib.auth import authenticate, login
from .models import Admin, Hotel, Amenity, RoomTypes, Rooms, RateAmenity
from django.contrib.auth.models import User

from django.views.generic import DetailView


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
                return HttpResponseRedirect('/enter/homepage/')
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
            return HttpResponseRedirect('/enter/login/')
        context = {'form': form}
        return render(request, 'registration.html', context)


###########################################################
'''главная страница, где отображаются уже 
зарегистрированные им отели со следующим описанием - (название отеля, координаты отеля) 
и две кнопки возле каждого отеля Delete, Details'''


class HomePageView(View):

    def get(self, request):

        form = DeleteForm(request.POST or None)

        user = request.session['data']
        user = User.objects.get(username=user)

        hotels = Hotel.objects.filter(admin=user)
        context = {'user': user, 'hotels': hotels, 'form': form}
        return render(request, "homepage.html", context)

    def post(self, request, *args, **kwargs):
        form = DeleteForm(request.POST or None)
        if form.is_valid():
            user = request.session['data']
            user = User.objects.get(username=user)
            hotelname = form.cleaned_data['hotelname']
            hotels = Hotel.objects.filter(admin=user)
            for hotel in hotels:
                if hotel.hotel_name == hotelname:
                    hotel.delete()
                    hotels = Hotel.objects.filter(admin=user)
                    context = {'user': user, 'hotels': hotels, 'form': form}
                    return render(request, "homepage.html", context)
        user = request.session['data']
        user = User.objects.get(username=user)
        hotels = Hotel.objects.filter(admin=user)
        context = {'user': user, 'hotels': hotels, 'form': form}
        return render(request, "homepage.html", context)


class CreateRoom(View):

    def get(self, request, slug):

        form = CreateRoomForm(request.POST or None)

        user = request.session['data']
        user = User.objects.get(username=user)

        hotel = Hotel.objects.get(admin=user, url=slug)
        amenities = Amenity.objects.filter(hotel=hotel)
        room_types = RoomTypes.objects.filter(hotel=hotel)

        context = {'hotel': hotel, 'form': form, 'user': user, 'amenities': amenities, 'room_types': room_types}
        return render(request, "createroom.html", context)

    def post(self, request, slug):

        #сделать проверку на заполнение всех полей (проверка dropdown)
        user = request.session['data']
        user = User.objects.get(username=user)

        amenities = request.POST.getlist('amenity')
        hotel = Hotel.objects.get(admin=user, url=slug)

        for amenity in amenities:
            am = Amenity.objects.get(hotel=hotel, amenity_name=amenity)
            total =+ am.amenity_price

        room_number = request.POST.get('room_number')

        room_type = request.POST.get('dropdown')
        room_type = RoomTypes.objects.get(room_type_name=room_type)

        room_rate_price = room_type.room_type_price + total
        room = Rooms(room_number=room_number, room_type=room_type, hotel=hotel, room_rate_price=room_rate_price)
        room.save()

        for amenity in amenities:
            am = Amenity.objects.get(hotel=hotel, amenity_name=amenity)
            rate_amenity = RateAmenity(room=room, amenity=am)
            rate_amenity.save()

        return HttpResponseRedirect('/enter/homepage/')


class AddHotelView(View):

    def get(self, request, *args, **kwargs):
        form = AddHotelForm(request.POST or None)
        context = {'form': form}
        return render(request, 'add_hotel.html', context)

    def post(self, request, *args, **kwargs):
        form = AddHotelForm(request.POST or None)
        user = request.session['data']
        user = User.objects.get(username=user)
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

            return HttpResponseRedirect('/enter/homepage/')
        context = {'form': form}
        return render(request, 'add_hotel.html', context)


class HotelDetailView(View):
    #model = Hotel
    #slug_field = "url"

    def get(self, request, slug):
        hotel = Hotel.objects.get(url=slug)
        #request.session['hotel_name'] = hotel.hotel_name
        amenities = Amenity.objects.filter(hotel=hotel)
        context = {"hotel": hotel, "amenities": amenities}
        return render(request, "hotel_detail.html", context)


class CreateAmenityView(View):

    def get(self, request, slug):

        form = CreateAmenityForm(request.POST or None)

        user = request.session['data']
        user = User.objects.get(username=user)

        hotel = Hotel.objects.get(url=slug)

        context = {'user': user, 'hotel': hotel, 'form': form}
        return render(request, "createamenity.html", context)

    def post(self, request, slug):
        form = CreateAmenityForm(request.POST or None)
        user = request.session['data']

        user = User.objects.get(username=user)

        if form.is_valid():

            hotel = Hotel.objects.get(url=slug, admin=user)

            amenity = form.save(commit=False)
            amenity.amenity_name = form.cleaned_data['amenity_name']
            amenity.amenity_price = form.cleaned_data['amenity_price']
            amenity.hotel = hotel
            amenity.save()

            # succes new amenity
            return HttpResponseRedirect('/enter/homepage/')
        hotel = Hotel.objects.get(url=slug)
        context = {'user': user, 'hotel': hotel, 'form': form}
        return render(request, "createamenity.html", context)



