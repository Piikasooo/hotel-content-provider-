from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from .forms import LoginForm, RegistrationForm
from django.contrib.auth import authenticate, login
from .models import Admin
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


class LoginView(View):

    def get(self, request, *args, **kwargs):
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
                return HomePageView().get(request, data=user.username)
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
            return HomePageView().get(request, data=user.username)
        context = {'form': form}
        return render(request, 'registration.html', context)


###########################################################
'''главная страница, где отображаются уже 
зарегистрированные им отели со следующим описанием - (название отеля, координаты отеля) 
и две кнопки возле каждого отеля Delete, Details'''


class HomePageView(View):

    def get(self, request, data):
        user = data
        user = User.objects.get(username=user)

        admin = User.objects.all()
        context = {'admin': admin, 'user': user}
        return render(request, "homepage.html", context)
