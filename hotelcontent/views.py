from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from .forms import LoginForm, RegistrationForm, DeleteForm, CreateRoomForm, AddHotelForm
from django.contrib.auth import authenticate, login
from .models import Admin, Hotel
from django.contrib.auth.models import User


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

    def get(self, request, *args, **kwargs):

        form = CreateRoomForm(request.POST or None)

        user = request.session['data']
        user = User.objects.get(username=user)

        hotels = Hotel.objects.filter(admin=user)
        context = {'hotels': hotels, 'form': form}
        return render(request, "createroom.html", context)


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

            new_hotel.save()

            return HttpResponseRedirect('/enter/homepage/')
        context = {'form': form}
        return render(request, 'add_hotel.html', context)




