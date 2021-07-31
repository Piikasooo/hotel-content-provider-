from django import forms
from django.contrib.auth.models import User
from .models import Hotel, RoomTypes, Rooms


class AddRoomForm(forms.ModelForm):

    hotel = forms.CharField(max_length=120)
    room_type = forms.CharField(max_length=120)
    room_number = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hotel'].label = 'Введите название отеля'
        self.fields['room_type'].label = 'Введите тип комнаты'
        self.fields['room_number'].label = 'Введите номер комнаты'

    def clean_hotel(self):
        hotel = self.cleaned_data['hotel']
        if not Hotel.objects.filter(hotel_name=hotel).exists():
            raise forms.ValidationError(f'Отель с даным названием "{hotel}" не найден в системе')
        return self.hotel

    def clean_room_type(self):
        room_type = self.cleaned_data['room_type']
        if not RoomTypes.objects.filter(hotel_type_name=room_type).exists():
            raise forms.ValidationError(f'Тип комнаты с даным названием "{room_type}" не найден в системе')
        return self.room_type

    class Meta:
        model = Rooms
        fields = ['hotel', 'room_type', 'room_number']


class DeleteForm(forms.ModelForm):

    hotelname = forms.CharField(max_length=200)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hotelname'].label = 'Введите название отеля'

    def clean(self):
        hotelname = self.cleaned_data['hotelname']

# фильтровать только отели самого админа
        if not Hotel.objects.filter(hotel_name=hotelname).exists():
            raise forms.ValidationError(f'Отель с даным названием "{hotelname}" не найден в системе')
        return self.cleaned_data

    class Meta:
        model = Hotel
        fields = ['hotelname']


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
    hotel_long = forms.DecimalField(max_digits=9, decimal_places=6, required=True)
    hotel_lat = forms.DecimalField(max_digits=9, decimal_places=6, required=True)
    hotel_email = forms.EmailField(required=True)
    hotel_url = forms.URLField(required=True)
    hotel_description = forms.TextInput()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hotel_name'].label = 'Название'
        self.fields['hotel_long'].label = 'Долгота'
        self.fields['hotel_lat'].label = 'Широта'
        self.fields['hotel_email'].label = 'Электронная почта'
        self.fields['hotel_url'].label = 'Сайт'
        self.fields['hotel_description'].label = 'Описание'

    def clean(self):
        hotel_name = self.cleaned_data['hotel_name']
        hotel_long = self.cleaned_data['hotel_long']
        hotel_lat = self.cleaned_data['hotel_lat']
        hotel_email = self.cleaned_data['hotel_email']
        hotel_url = self.cleaned_data['hotel_url']
        hotel_description = self.cleaned_data['hotel_description']

        if Hotel.objects.filter(hotel_long=hotel_long, hotel_lat=hotel_lat).exists():
            raise forms.ValidationError(f'Отель по координатам {hotel_lat}, {hotel_long} уже зарегистрирован!')
        elif Hotel.objects.filter(hotel_email=hotel_email).exists():
            raise forms.ValidationError(f'Отель с электронным адресом {hotel_email} уже зарегистрирован!')
        elif Hotel.objects.filter(hotel_url=hotel_url).exists():
            raise forms.ValidationError(f'Отель с сайтом {hotel_url} уже зарегистрирован!')

        return self.cleaned_data

    class Meta:
        model = Hotel
        fields = ['hotel_name', 'hotel_long', 'hotel_lat', 'hotel_email', 'hotel_url', 'hotel_description']


