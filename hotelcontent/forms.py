from django import forms
from django.contrib.auth.models import User
from .models import Hotel, RoomTypes, Amenity, Coefficient, Rooms
from .models import Hotel, RoomTypes, Amenity, Coefficient, Rooms, HotelsImages
from datetime import date


class CreateAmenityForm(forms.ModelForm):
    amenity_name = forms.CharField(max_length=200)
    amenity_price = forms.DecimalField(max_digits=7, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amenity_name'].label = 'Введите название amenity'
        self.fields['amenity_price'].label = 'Введите цену за amenity'

    class Meta:
        model = Amenity
        fields = ['amenity_name', 'amenity_price']


class CreateCoefficientForm(forms.ModelForm):

    start_date = forms.DateField()
    end_date = forms.DateField()
    coefficient = forms.DecimalField(max_digits=7, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date'].label = 'Введите начало периода'
        self.fields['end_date'].label = 'Введите конец периода'
        self.fields['coefficient'].label = 'Введите коефициент'

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if start_date < date.today():
            raise forms.ValidationError(f'Начальная дата выбрана некоректно')
        return start_date

    def clean_end_date(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if start_date > end_date:
            raise forms.ValidationError(f'Конечная дата выбрана некоректно')
        return end_date

    def clean(self):
        coefficient = self.cleaned_data.get('coefficient')
        if coefficient < 0:
            raise forms.ValidationError(f'Коефицент введен неверно')
        return self.cleaned_data

    class Meta:
        model = Coefficient
        fields = ['start_date', 'end_date', 'coefficient']


class CreateRoomForm(forms.ModelForm):
    hotel = forms.CharField(max_length=120)
    room_type = forms.CharField(max_length=120)
    room_number = forms.IntegerField()
    room_price = forms.DecimalField(max_digits=6, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['room_type'].label = 'Введите тип комнаты'
        self.fields['room_number'].label = 'Введите номер комнаты'

    def clean_end_date(self):
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']
        if start_date > end_date:
            raise forms.ValidationError(f'Конечная дата выбрана некоректно')
        return start_date

    def clean(self):
        coefficient = self.cleaned_data['coefficient']
        if coefficient < 0:
            raise forms.ValidationError(f'Коефицент введен неверно')
        return self.cleaned_data

    class Meta:
        model = Rooms
        fields = ['room_type', 'room_number', 'room_price']


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
    hotel_name = forms.CharField(required=True, label='Название')
    hotel_long = forms.DecimalField(max_digits=9, decimal_places=6, required=True, label='Долгота')
    hotel_lat = forms.DecimalField(max_digits=9, decimal_places=6, required=True, label='Широта')
    hotel_email = forms.EmailField(required=True, label='Электронная почта')
    hotel_url = forms.URLField(required=True, label='Сайт')
    hotel_description = forms.TextInput()
    hotel_image = forms.ImageField(label='Фото')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hotel_description'].label = 'Описание'

    def clean(self):
        hotel_name = self.cleaned_data.get('hotel_name')
        hotel_long = self.cleaned_data.get('hotel_long')
        hotel_lat = self.cleaned_data.get('hotel_lat')
        hotel_email = self.cleaned_data.get('hotel_email')
        hotel_url = self.cleaned_data.get('hotel_url')
        hotel_description = self.cleaned_data.get('hotel_description')

        if Hotel.objects.filter(hotel_long=hotel_long, hotel_lat=hotel_lat).exists():
            raise forms.ValidationError(f'Отель по координатам {hotel_lat}, {hotel_long} уже зарегистрирован!')
        elif Hotel.objects.filter(hotel_email=hotel_email).exists():
            raise forms.ValidationError(f'Отель с электронным адресом {hotel_email} уже зарегистрирован!')
        elif Hotel.objects.filter(hotel_url=hotel_url).exists():
            raise forms.ValidationError(f'Отель с сайтом {hotel_url} уже зарегистрирован!')

        return self.cleaned_data

    class Meta:
        model = Hotel
        fields = ['hotel_name', 'hotel_long', 'hotel_lat', 'hotel_email',
                  'hotel_url', 'hotel_description', 'hotel_image']


class AddRoomTypeForm(forms.ModelForm):
    room_type_name = forms.CharField(max_length=200, required=True)
    room_type_description = forms.CharField(max_length=200, required=True)
    room_type_price = forms.DecimalField(max_digits=6, decimal_places=2, required=True)
    hotel_field = ''

    def __init__(self, hotel, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['room_type_name'].label = 'Введите название для типа комнаты'
        self.fields['room_type_description'].label = 'Введите описание для даного типа комнаты'
        self.fields['room_type_price'].label = 'Введите цену даного типа комнаты'
        self.hotel_field = hotel

    def clean(self):
        room_type_name = self.cleaned_data.get('room_type_name')
        room_type_description = self.cleaned_data.get('room_type_description')
        room_type_price = self.cleaned_data.get('room_type_price')
        hotel = Hotel.objects.get(hotel_url=self.hotel_field)

        if RoomTypes.objects.filter(room_type_name=room_type_name, hotel=hotel).exists():
            raise forms.ValidationError(f'Room type with a name {room_type_name}  already exists!')

        return self.cleaned_data

    class Meta:
        model = RoomTypes
        fields = ['room_type_name', 'room_type_description', 'room_type_price']


class AddHotelImagesForm(forms.ModelForm):
    hotel_photo = forms.ImageField(label='Photo', required=True)
    photo_description = forms.CharField(max_length=50, required=True)

    hotel_field = ''

    def __init__(self, hotel, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hotel_field = hotel

    class Meta:
        model = HotelsImages
        fields = ['hotel_photo', 'photo_description']
