from django import forms
from django.contrib.auth.models import User
from .models import Hotel, RoomTypes, Amenity, Coefficient, HotelsImages
from datetime import date


class CreateAmenityForm(forms.ModelForm):
    amenity_name = forms.CharField(max_length=200)
    amenity_price = forms.DecimalField(max_digits=7, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amenity_name'].label = 'Enter amenity name'
        self.fields['amenity_price'].label = 'Enter amenity price'

    class Meta:
        model = Amenity
        fields = ['amenity_name', 'amenity_price']


class CreateCoefficientForm(forms.ModelForm):

    start_date = forms.DateField()
    end_date = forms.DateField()
    coefficient = forms.DecimalField(max_digits=7, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date'].label = 'Enter start date'
        self.fields['end_date'].label = 'Enter end date'
        self.fields['coefficient'].label = 'Enter coefficient'

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if start_date < date.today():
            raise forms.ValidationError(f'Start date is invalid')
        return start_date

    def clean_end_date(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if start_date > end_date:
            raise forms.ValidationError(f'End date is invalid')
        return end_date

    def clean(self):
        coefficient = self.cleaned_data.get('coefficient')
        if coefficient < 0:
            raise forms.ValidationError(f'Coefficient is invalid')
        return self.cleaned_data

    class Meta:
        model = Coefficient
        fields = ['start_date', 'end_date', 'coefficient']


class DeleteForm(forms.ModelForm):

    hotelname = forms.CharField(max_length=200)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hotelname'].label = 'Enter hotel name'

    def clean(self):
        hotelname = self.cleaned_data['hotelname']

        # фильтровать только отели самого админа
        if not Hotel.objects.filter(hotel_name=hotelname).exists():
            raise forms.ValidationError(f"Hotel with name '{hotelname}' doesn't exist")
        return self.cleaned_data

    class Meta:
        model = Hotel
        fields = ['hotelname']


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['password'].label = 'Password'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f"User with username '{username}' doesn't exist")
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
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
        self.fields['username'].label = 'Username'
        self.fields['password'].label = 'Password'
        self.fields['confirm_password'].label = 'Confirm password'
        self.fields['phone'].label = 'Phone number'
        self.fields['first_name'].label = 'First name'
        self.fields['last_name'].label = 'Last name'
        self.fields['address'].label = 'Address'
        self.fields['email'].label = 'Email'

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'This email address is already in use')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Username {username} is already in use')
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError(f'Password mismatch')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password',
                  'phone', 'first_name', 'last_name', 'address', 'email']


class AddHotelForm(forms.ModelForm):
    hotel_name = forms.CharField(required=True, label='Hotel name')
    hotel_long = forms.DecimalField(max_digits=9, decimal_places=6, required=True, label='Longitude')
    hotel_lat = forms.DecimalField(max_digits=9, decimal_places=6, required=True, label='Latitude')
    hotel_email = forms.EmailField(required=True, label='Email')
    hotel_url = forms.URLField(required=True, label='Hotel site')
    hotel_description = forms.TextInput()
    hotel_image = forms.ImageField(label='Hotel photo')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hotel_description'].label = 'Hotel description'

    def clean(self):
        hotel_long = self.cleaned_data.get('hotel_long')
        hotel_lat = self.cleaned_data.get('hotel_lat')
        hotel_email = self.cleaned_data.get('hotel_email')
        hotel_url = self.cleaned_data.get('hotel_url')

        if Hotel.objects.filter(hotel_long=hotel_long, hotel_lat=hotel_lat).exists():
            raise forms.ValidationError(f'Hotel with coordinates {hotel_lat}, {hotel_long} is already in use!')
        elif Hotel.objects.filter(hotel_email=hotel_email).exists():
            raise forms.ValidationError(f'Hotel with email {hotel_email} is already in use!')
        elif Hotel.objects.filter(hotel_url=hotel_url).exists():
            raise forms.ValidationError(f'Hotel with site {hotel_url} is already in use!')

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
        self.fields['room_type_name'].label = 'Enter room type name'
        self.fields['room_type_description'].label = 'Enter room type description'
        self.fields['room_type_price'].label = 'Enter room type price per night'
        self.hotel_field = hotel

    def clean(self):
        room_type_name = self.cleaned_data.get('room_type_name')
        room_type_description = self.cleaned_data.get('room_type_description')
        room_type_price = self.cleaned_data.get('room_type_price')
        hotel = Hotel.objects.get(hotel_url=self.hotel_field)

        if RoomTypes.objects.filter(room_type_name=room_type_name, hotel=hotel).exists():
            raise forms.ValidationError(f'Room type with a name {room_type_name} already exists!')

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
