from django import forms
from django.contrib.auth.models import User

from .models import Hotel


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Пользователь с логином "{username}" не найден в системе')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError('Неверный пароль')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password']


class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(required=False)
    address = forms.CharField(required=False)
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Подтвердите пароль'
        self.fields['phone'].label = 'Номер телефона'
        self.fields['first_name'].label = 'Ваше имя'
        self.fields['last_name'].label = 'Ваша фамилия'
        self.fields['address'].label = 'Адрес'
        self.fields['email'].label = 'EMAIL'

    def clean_email(self):
        email = self.cleaned_data['email']
        domain = email.split('.')[-1]
        if domain in ['com', 'net']:
            raise forms.ValidationError(f'Регистрация для домена "{domain}" невозможна')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'Данный почтовый адресс уже зарегестрирован')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Имя {username} занято')
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError(f'Пароли не совпадают')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password',
                  'phone', 'first_name', 'last_name', 'address', 'email']


class AddHotelForm(forms.ModelForm):
    hotel_name = forms.CharField(required=True)
    hotel_address = forms.CharField(required=True)
    hotel_email = forms.EmailField(required=True)
    hotel_url = forms.URLField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hotel_name'].label = 'Название'
        self.fields['hotel_address'].label = 'Адрес'
        self.fields['hotel_email'].label = 'Электронная почта'
        self.fields['hotel_url'].label = 'Сайт'

    def clean_hotel_address(self):
        hotel_address = self.cleaned_data['hotel_address']
        if Hotel.objects.filter(hotel_address=hotel_address).exists():
            raise forms.ValidationError(f'Отель по адресу {hotel_address} уже зарегистрирован!')
        return hotel_address

    class Meta:
        model = Hotel
        fields = ['hotel_name', 'hotel_address', 'hotel_email', 'hotel_url']