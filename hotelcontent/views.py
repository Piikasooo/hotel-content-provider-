from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View

from .forms import LoginForm, RegistrationForm, DeleteForm, CreateCoefficientForm, AddHotelForm, AddHotelImagesForm, \
    CreateAmenityForm, AddRoomTypeForm
from .models import Admin, Hotel, Amenity, RoomTypes, Rooms, RateAmenity, HotelsImages
from .models import Coefficient, Bookings


class LoginView(View):

    def get(self, request):

        try:
            del request.session['data']
            form = LoginForm(request.POST or None)
            context = {'form': form}
            return render(request, 'login.html', context)
        except KeyError:
            form = LoginForm(request.POST or None)
            context = {'form': form}
            return render(request, 'login.html', context)

    def post(self, request):
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

    def get(self, request):
        form = RegistrationForm(request.POST or None)
        context = {'form': form}
        return render(request, 'registration.html', context)

    def post(self, request):
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

        if not authentication(request):
            alert = 'Please, login first'
            messages.info(request, alert)
            return HttpResponseRedirect('/login/')

        form = DeleteForm(request.POST or None)

        user = request.user

        hotels = Hotel.objects.filter(admin=user)
        context = {
            'user': user,
            'hotels': hotels,
            'form': form
        }
        return render(request, "hotels.html", context)


class CreateRoom(View):

    def get(self, request, slug):

        if not authentication(request):
            alert = 'Please, login first'
            messages.info(request, alert)
            return HttpResponseRedirect('/login/')

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
            alert = 'Select amenity'
            messages.info(request, alert)
            route = '/add_room/{0}/'.format(hotel.url)
            return HttpResponseRedirect(route)

        total = 0
        for amenity in amenities:
            amenity_name = amenity.split('/')[0]
            am = Amenity.objects.get(hotel=hotel, amenity_name=amenity_name)
            total = total + am.amenity_price

        room_number = request.POST.get('room_number')
        allrooms = Rooms.objects.filter(hotel=hotel)

        for roomhotel in allrooms:
            try:
                if roomhotel.room_number == int(room_number):
                    alert = 'Room number is exist'
                    messages.info(request, alert)
                    route = '/add_room/{0}/'.format(hotel.url)
                    return HttpResponseRedirect(route)
            except:
                alert = 'Enter room number!'
                messages.info(request, alert)
                route = '/add_room/{0}/'.format(hotel.url)
                return HttpResponseRedirect(route)

        room_type = request.POST.get('dropdown')
        if str(room_type) == 'Select type room':
            alert = 'Select type room'
            messages.info(request, alert)
            route = '/add_room/{0}/'.format(hotel.url)
            return HttpResponseRedirect(route)

        room_type_name = room_type.split('/')[0]
        room_type = RoomTypes.objects.get(room_type_name=room_type_name, hotel=hotel)
        try:
            room_rate_price = room_type.room_type_price + total
            room = Rooms(room_number=room_number, room_type=room_type, hotel=hotel, room_rate_price=room_rate_price)
            room.save()
        except ValueError:
            alert = 'Incorrect value for number'
            messages.info(request, alert)
            return HttpResponseRedirect('/homepage/')

        for amenity in amenities:
            amenity_name = amenity.split('/')[0]
            am = Amenity.objects.get(hotel=hotel, amenity_name=amenity_name)
            rate_amenity = RateAmenity(room=room, amenity=am)
            rate_amenity.save()

        alert = 'Successfully created new room'
        messages.info(request, alert)
        route = '/rooms/{0}/'.format(hotel.url)
        return HttpResponseRedirect(route)


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
            new_hotel.hotel_image = form.cleaned_data['hotel_image']

            hotelname = ''.join(form.cleaned_data['hotel_name'].split())
            url = hotelname + 'Hotel'
            new_hotel.url = url
            new_hotel.save()
            return new_hotel

    def get(self, request):

        if not authentication(request):
            alert = 'Please, login first'
            messages.info(request, alert)
            return HttpResponseRedirect('/login/')

        form = AddHotelForm(request.POST or None)
        context = {'form': form}
        return render(request, 'add_hotel.html', context)

    def post(self, request):
        form = AddHotelForm(request.POST, request.FILES)
        user = request.user
        if self._create_hotel(form, user):
            return HttpResponseRedirect('/homepage/')
        context = {'form': form}
        return render(request, 'add_hotel.html', context)


class HotelDetailView(View):

    def get(self, request, slug):
        if not authentication(request):
            alert = 'Please, login first'
            messages.info(request, alert)
            return HttpResponseRedirect('/login/')

        hotel = Hotel.objects.get(url=slug)
        images = HotelsImages.objects.filter(hotel=hotel)
        context = {'hotel': hotel, 'photos': images}
        return render(request, "hotel_detail.html", context)

    def post(self, request, slug):
        hotel = Hotel.objects.get(url=slug)
        hotel.delete()
        alert = 'Hotel is deleted'
        messages.info(request, alert)
        return HttpResponseRedirect('/homepage/')


class CreateAmenityView(View):

    def get(self, request, slug):

        if not authentication(request):
            alert = 'Please, login first'
            messages.info(request, alert)
            return HttpResponseRedirect('/login/')

        form = CreateAmenityForm(request.POST or None)

        user = request.session['data']
        user = User.objects.get(username=user)

        hotel = Hotel.objects.get(url=slug, admin=user)

        amenities = Amenity.objects.filter(hotel=hotel)
        context = {'user': user, 'hotel': hotel, 'form': form, 'amenities': amenities}
        return render(request, "createamenity.html", context)

    def post(self, request, slug):

        form = CreateAmenityForm(request.POST or None)
        user = request.session['data']

        user = User.objects.get(username=user)

        if form.is_valid():
            hotel = Hotel.objects.get(url=slug, admin=user)
            amenity = form.save(commit=False)
            amenity_name = form.cleaned_data['amenity_name']
            if Amenity.objects.filter(hotel=hotel, amenity_name=amenity_name).exists():
                alert = 'This amenity name is already exists'
                messages.info(request, alert)
                return HttpResponseRedirect('/amenity/' + hotel.url + '/')

            amenity.amenity_name = amenity_name
            amenity.amenity_price = form.cleaned_data['amenity_price']
            amenity.hotel = hotel
            amenity.save()
            alert = 'Successfully created new amenity'
            messages.info(request, alert)
            return HttpResponseRedirect('/amenity/' + hotel.url + '/')


class CreateCoefficientView(View):

    def get(self, request, slug):

        if not authentication(request):

            alert = 'Please, login first'
            messages.info(request, alert)
            return HttpResponseRedirect('/login/')

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
        try:
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
        except:
            alert = 'Incorrect start_date'
            messages.info(request, alert)
            route = '/coefficient/{0}/'.format(hotel.url)
            return HttpResponseRedirect(route)


class RoomsView(View):

    def get(self, request, slug):
        if not authentication(request):
            alert = 'Please, login first'
            messages.info(request, alert)
            return HttpResponseRedirect('/login/')

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

        if not authentication(request):
            alert = 'Please, login first'
            messages.info(request, alert)
            return HttpResponseRedirect('/login/')

        user = request.user

        hotel = Hotel.objects.get(url=slug)
        form = AddRoomTypeForm(hotel.hotel_url, request.POST or None)

        room_type = RoomTypes.objects.filter(hotel=hotel)
        context = {
            'user': user,
            'hotel': hotel,
            'form': form,
            'room_type': room_type
        }
        return render(request, "add_room_type.html", context)

    def post(self, request, slug):
        user = request.user
        hotel = Hotel.objects.get(url=slug, admin=user)

        form = AddRoomTypeForm(hotel.hotel_url, request.POST or None)

        if form.is_valid():
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

        if not authentication(request):
            alert = 'Please, login first'
            messages.info(request, alert)
            return HttpResponseRedirect('/login/')

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


class HotelUpdateView(View):

    def get(self, request, slug):

        if not authentication(request):
            alert = 'Please, login first'
            messages.info(request, alert)
            return HttpResponseRedirect('/login/')

        hotel = Hotel.objects.get(url=slug)
        context = {"hotel": hotel}
        return render(request, "hotel_update.html", context)

    def post(self, request, slug):
        hotel = Hotel.objects.get(url=slug)

        hotel.hotel_name = request.POST.get('name')
        hotel.hotel_long = float(request.POST.get('long'))
        hotel.hotel_lat = float(request.POST.get('lat'))
        hotel.hotel_email = request.POST.get('email')
        hotel.hotel_url = request.POST.get('url')
        hotel.hotel_description = request.POST.get('description')
        if not request.FILES.get('img'):
            hotelname = ''.join(hotel.hotel_name.split())

            url = hotelname + 'Hotel'
            hotel.url = url
            hotel.save()
        else:
            hotel.hotel_image = request.FILES.get('img')
            hotelname = ''.join(hotel.hotel_name.split())

            url = hotelname + 'Hotel'
            hotel.url = url
            hotel.save()

        bookings_hotels = list(Bookings.objects.filter(hotels=hotel))
        for booking in bookings_hotels:
            booking.hotel = hotel.hotel_name
            booking.save()
        alert = 'Successfully update Hotel'
        messages.info(request, alert)
        return HttpResponseRedirect('/homepage/')


class AmenityUpdate(View):

    def get(self, request, slug, amenity_name):
        try:
            if not authentication(request):
                alert = 'Please, login first'
                messages.info(request, alert)
                return HttpResponseRedirect('/login/')

            hotel = Hotel.objects.get(url=slug)
            amenity = Amenity.objects.get(hotel=hotel, amenity_name=amenity_name)
            context = {"hotel": hotel, "amenity": amenity}
            return render(request, "amenity_update.html", context)
        except:
            hotel = Hotel.objects.get(url=slug)
            route = '/amenity/{0}/'.format(hotel.url)
            return HttpResponseRedirect(route)

    def post(self, request, slug, amenity_name):

        hotel = Hotel.objects.get(url=slug)
        amenity = Amenity.objects.get(hotel=hotel, amenity_name=amenity_name)

        if request.POST.get("update"):
            amenity.amenity_name = request.POST.get("amenity_name")
            amenity.amenity_price = request.POST.get("amenity_price")
            amenity.save()
            alert = 'Successfully update amenity {0}'.format(amenity_name)
            messages.info(request, alert)
            route = '/amenity/{0}/'.format(hotel.url)
            return HttpResponseRedirect(route)
        else:
            amenity_id = request.POST.get("delete")
            amenity_for_del = Amenity.objects.get(id=amenity_id)
            amenity_for_del.delete()
            alert = 'Successfully deleted amenity'
            messages.info(request, alert)
            route = '/amenity/{0}/'.format(hotel.url)
            return HttpResponseRedirect(route)


class TypeRoomUpdate(View):

    def get(self, request, slug, room_type_name):

            if not authentication(request):
                alert = 'Please, login first'
                messages.info(request, alert)
                return HttpResponseRedirect('/login/')

            hotel = Hotel.objects.get(url=slug)
            room_type = RoomTypes.objects.get(hotel=hotel, room_type_name=room_type_name)
            context = {"hotel": hotel, "room_type": room_type}
            return render(request, "room_type_update.html", context)

            hotel = Hotel.objects.get(url=slug)
            route = '/add_room_type/{0}/'.format(hotel.url)
            return HttpResponseRedirect(route)

    def post(self, request, slug, room_type_name):

        hotel = Hotel.objects.get(url=slug)
        room_type = RoomTypes.objects.get(hotel=hotel, room_type_name=room_type_name)

        if request.POST.get("update"):
            room_type.room_type_name = request.POST.get("room_type_name")
            room_type.room_type_description = request.POST.get("room_type_description")
            room_type.room_type_price = request.POST.get("room_type_price")
            room_type.save()
            alert = 'Successfully update type room {0}'.format(room_type_name)
            messages.info(request, alert)
            route = '/add_room_type/{0}/'.format(hotel.url)
            return HttpResponseRedirect(route)
        else:
            room_type_id = request.POST.get("delete")
            room_type_del = RoomTypes.objects.get(id=room_type_id)
            room_type_del.delete()
            alert = 'Successfully delete type room'
            messages.info(request, alert)
            route = '/add_room_type/{0}/'.format(hotel.url)
            return HttpResponseRedirect(route)


class CoefficientUpdate(View):

    def get(self, request, slug, id):

        if not authentication(request):
            alert = 'Please, login first'
            messages.info(request, alert)
            return HttpResponseRedirect('/login/')

        hotel = Hotel.objects.get(url=slug)
        coefficient = Coefficient.objects.get(id=id)
        context = {"hotel": hotel, "coefficient": coefficient}
        return render(request, "coefficient_update.html", context)

    def post(self, request, slug, id):

        hotel = Hotel.objects.get(url=slug)
        coefficient = Coefficient.objects.get(id=id)
        try:
            if request.POST.get("update"):
                coefficient.start_date = request.POST.get("start_date")
                coefficient.end_date = request.POST.get("end_date")
                coefficient.coefficient = request.POST.get("coefficient")
                coefficient.save()
                alert = 'Successfully update coefficient'
                messages.info(request, alert)
                route = '/coefficient/{0}/'.format(hotel.url)
                return HttpResponseRedirect(route)
            else:
                coefficient.delete()
                alert = 'Successfully delete coefficient'
                messages.info(request, alert)
                route = '/coefficient/{0}/'.format(hotel.url)
                return HttpResponseRedirect(route)
        except:
            alert = 'Incorrect data'
            messages.info(request, alert)
            route = '/coefficient/{0}/'.format(hotel.url)
            return HttpResponseRedirect(route)


class RateUpdateView(View):

    def get(self, request, slug, room_number):

        if not authentication(request):
            alert = 'Please, login first'
            messages.info(request, alert)
            return HttpResponseRedirect('/login/')

        user = request.session['data']
        user = User.objects.get(username=user)

        hotel = Hotel.objects.get(admin=user, url=slug)
        amenities = list(Amenity.objects.filter(hotel=hotel))
        room_types = list(RoomTypes.objects.filter(hotel=hotel))
        room = Rooms.objects.get(hotel=hotel, room_number=room_number)
        rate_amenities = list(RateAmenity.objects.filter(room=room))
        for rate_amenity in rate_amenities:
            amenities.remove(rate_amenity.amenity)
        room_types.remove(room.room_type)
        context = {'hotel': hotel, 'room': room, 'user': user, 'rate_amenities': rate_amenities, 'amenities': amenities, 'room_types': room_types}
        return render(request, "rate_update.html", context)

    def post(self, request, slug, room_number):

        user = request.session['data']
        user = User.objects.get(username=user)

        hotel = Hotel.objects.get(admin=user, url=slug)
        room = Rooms.objects.get(hotel=hotel, room_number=room_number)

        if request.POST.get("update"):

            amenities = request.POST.getlist('amenity')

            if len(amenities) == 0:
                alert = 'Select amenity'
                messages.info(request, alert)
                route = '/room/{0}/{1}'.format(hotel.url, room.room_number)
                return HttpResponseRedirect(route)

            room_number = request.POST.get('room_number')
            allrooms = Rooms.objects.exclude(room_number=room.room_number).filter(hotel=hotel)
            print(allrooms)
            for roomhotel in allrooms:
                if roomhotel.room_number == int(room_number):
                    alert = 'Room number is already exists'
                    messages.info(request, alert)
                    route = '/room/{0}/{1}'.format(hotel.url, room.room_number)
                    return HttpResponseRedirect(route)

            total = 0
            for amenity in amenities:
                am = Amenity.objects.get(hotel=hotel, amenity_name=amenity)
                total = total + am.amenity_price

            room_type = request.POST.get('dropdown')

            RateAmenity.objects.filter(room=room).delete()

            room_type_object = RoomTypes.objects.get(room_type_name=room_type, hotel=hotel)

            room_rate_price = room_type_object.room_type_price + total

            room.room_number = room_number
            room.room_type = room_type_object
            room.room_rate_price = room_rate_price
            room.save()

            bookings_room = Bookings.objects.filter(hotels=hotel, room=room, booking_stat=True)
            for booking in bookings_room:
                booking.room_number = room_number
                booking.save()

            for amenity in amenities:
                am = Amenity.objects.get(hotel=hotel, amenity_name=amenity)
                rate_amenity = RateAmenity(room=room, amenity=am)
                rate_amenity.save()

            alert = 'Successfully updated rate'
            messages.info(request, alert)
            route = '/rooms/{0}/'.format(hotel.url)
            return HttpResponseRedirect(route)

        else:
            room.delete()
            alert = 'Successfully deleted rate'
            messages.info(request, alert)
            route = '/rooms/{0}/'.format(hotel.url)
            return HttpResponseRedirect(route)


class AddHotelImage(View):

    def get(self, request, slug):

        if not authentication(request):
            alert = 'Please, login first'
            messages.info(request, alert)
            return HttpResponseRedirect('/login/')

        user = request.session['data']
        user = User.objects.get(username=user)

        hotel = Hotel.objects.get(url=slug)
        form = AddHotelImagesForm(hotel.hotel_url, request.POST or None)

        context = {
            'user': user,
            'hotel': hotel,
            'form': form,
        }
        return render(request, "add_photos.html", context)

    def post(self, request, slug):
        user = request.session['data']
        user = User.objects.get(username=user)
        hotel = Hotel.objects.get(url=slug, admin=user)
        form = AddHotelImagesForm(hotel.hotel_url, request.POST, request.FILES)

        if form.is_valid():
            hotel_image = form.save(commit=False)
            hotel_image.hotel_photo = form.cleaned_data['hotel_photo']
            hotel_image.photo_description = form.cleaned_data['photo_description']
            hotel_image.hotel = hotel
            hotel_image.save()

            return HttpResponseRedirect('/add_hotel_image/' + hotel.url + '/')

        context = {'user': user, 'hotel': hotel, 'form': form}
        return render(request, "add_photos.html", context)

# utils.py
def authentication(request):
    try:
        if request.session['data']:
            return True
    except KeyError:
        return False