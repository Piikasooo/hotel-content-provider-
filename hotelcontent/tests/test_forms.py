from django.contrib.auth.models import User
from django.test import TestCase, Client
from hotelcontent.forms import AddHotelForm, AddRoomTypeForm, RegistrationForm, LoginForm, DeleteForm, CreateRoomForm,\
    CreateCoefficientForm, CreateAmenityForm
from hotelcontent.models import Hotel, Admin, RoomTypes
from datetime import date ,timedelta
# print(f'{field} - {form.errors[field].as_text()}')


class TestCreateAmenityForm(TestCase):
    pass


class TestCreateCoefficientForm(TestCase):
    def test_create_coefficient_valid_form(self):
        coefficient_data = {
            'start_date': date.today(),
            'end_date': date.today() + timedelta(days=2),
            'coefficient': 3,
        }
        form = CreateCoefficientForm(data=coefficient_data)
        self.assertTrue(form.is_valid())

    def test_create_coefficient_no_valid_form(self):
        coefficient_data = {
            'start_date': date.today(),
            'end_date': date.today() - timedelta(days=2),
            'coefficient': -3,
        }
        form = CreateCoefficientForm(data=coefficient_data)
        errors_filed = {}
        for field in form.errors:
            errors_filed[field] = form.errors[field].as_text()
        self.assertEquals(errors_filed['end_date'],
                          '* Конечная дата выбрана некоректно')
        self.assertEquals(errors_filed['__all__'],
                          '* Коефицент введен неверно')


class TestCreateRoomForm(TestCase):
    def setUp(self):
        self.client = Client()
        self.credentials = {
            'username': 'tst',
            'password': 'QazxsW1234'}
        admin = User.objects.create_user(**self.credentials)
        Admin.objects.create(user=admin)

        self.hotel = Hotel.objects.create(
            hotel_name='setup_hotel',
            hotel_long=3.000012,
            hotel_lat=3.000103,
            hotel_email='setuptest@gmail.ua',
            hotel_url='http://www.testhotelurlsetup.net',
            hotel_description='some words',
            admin=admin,
            url='setup_hotelHotel'
        )

        self.room_type = RoomTypes.objects.create(
            room_type_name='setup_room_type_name',
            room_type_description='setup description text',
            room_type_price=100,
            hotel=self.hotel
        )

    def test_create_room(self):
        pass


class TestDeleteForm(TestCase):

    def setUp(self):
        self.client = Client()
        self.credentials = {
            'username': 'tst',
            'password': 'QazxsW1234'}
        admin = User.objects.create_user(**self.credentials)
        Admin.objects.create(user=admin)

        Hotel.objects.create(
            hotel_name='setup_hotel',
            hotel_long=3.000012,
            hotel_lat=3.000103,
            hotel_email='setuptest@gmail.ua',
            hotel_url='http://www.testhotelurlsetup.net',
            hotel_description='some words',
            admin=admin,
            url='setup_hotelHotel'
        )

    def test_delete_hotel_hotelname_not_exist(self):
        delete_data = {
            'hotelname': 'set5up_hotel',
        }
        form = DeleteForm(data=delete_data)
        errors_filed = {}
        for field in form.errors:
            errors_filed[field] = form.errors[field].as_text()
        self.assertFalse(form.is_valid())
        self.assertEquals(errors_filed['__all__'],
                          f'* Отель с даным названием "{delete_data["hotelname"]}" не найден в системе')


class TestLoginForm(TestCase):

    def setUp(self):
        self.client = Client()
        self.credentials = {
            'username': 'test_user',
            'password': 'QazxsW1234',
            'email': 'setuptest@gmail.ua',
        }
        User.objects.create_user(**self.credentials)

    def test_login_form_user_no_exist(self):
        login_data = {
            'username': 'test3_user',
            'password': 'Qazx4sW1234',
        }
        form = LoginForm(data=login_data)
        errors_filed = {}
        for field in form.errors:
            errors_filed[field] = form.errors[field].as_text()
        self.assertEquals(errors_filed['__all__'],
                          f'* Пользователь с логином "{login_data["username"]}" не найден в системе')

    def test_login_form_worng_password(self):
        login_data = {
            'username': 'test_user',
            'password': 'Qazx4sW1234',
        }
        form = LoginForm(data=login_data)
        errors_filed = {}
        for field in form.errors:
            errors_filed[field] = form.errors[field].as_text()
        self.assertEquals(errors_filed['__all__'],
                          f'* Неверный пароль')


class TestRegistrationForm(TestCase):

    def setUp(self):
        self.client = Client()
        self.credentials = {
            'username': 'test_user',
            'password': 'QazxsW1234',
            'email': 'setuptest@gmail.ua',
        }
        User.objects.create_user(**self.credentials)

    def test_registration_form_no_valid_data(self):
        registration_data = {
            'username': 'test_user',
            'password': 'QazxsW1234',
            'confirm_password': 'QazxsW1233',
            'phone': '',
            'first_name': '',
            'last_name': '',
            'address': '',
            'email': 'setuptest@gmail.ua',
        }
        form = RegistrationForm(data=registration_data)
        errors_filed = {}
        for field in form.errors:
            errors_filed[field] = form.errors[field].as_text()
        self.assertEquals(errors_filed['username'],
                          f'* Имя {registration_data["username"]} занято')
        self.assertEquals(errors_filed['email'],
                          '* Данный почтовый адресс уже зарегестрирован')
        self.assertEquals(errors_filed['__all__'],
                          '* Пароли не совпадают')


class TestAddHotelForm(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.credentials = {
            'username': 'tst',
            'password': 'QazxsW1234'}
        admin = User.objects.create_user(**self.credentials)
        Admin.objects.create(user=admin)

        Hotel.objects.create(
            hotel_name='setup_hotel',
            hotel_long=3.000012,
            hotel_lat=3.000103,
            hotel_email='setuptest@gmail.ua',
            hotel_url='http://www.testhotelurlsetup.net',
            hotel_description='some words',
            admin=admin,
            url='setup_hotelHotel'
        )

    def test_add_hotel_form_no_valid_url(self):
        user = User.objects.get(username='tst')
        Hotel.objects.create(
            hotel_name='hotel_test',
            hotel_long=3.000002,
            hotel_lat=3.000003,
            hotel_email='emailfortest@gmail.net',
            hotel_url='http://www.testhotelurl.com',
            hotel_description='some words',
            admin=user
        )
        hotel_data = {
            'hotel_name': 'hotel_test_2',
            'hotel_long': 3.000402,
            'hotel_lat': 3.000043,
            'hotel_email': 'emailfortest@gmail.net',
            'hotel_url': 'http://www.testhotelurl.com',
            'hotel_description': 'some words',
        }
        form = AddHotelForm(data=hotel_data)
        self.assertFalse(form.is_valid())
        error = {}
        for field in form.errors:
            error[field] = form.errors[field].as_text()
        self.assertEquals(error['__all__'],
                          f'* Отель с электронным адресом {hotel_data["hotel_email"]} уже зарегистрирован!')

    def test_add_hotel_form_no_valid_hotel_email(self):
        user = User.objects.get(username='tst')
        Hotel.objects.create(
            hotel_name='hotel_test',
            hotel_long=3.000002,
            hotel_lat=3.000003,
            hotel_email='emailfortest@gmail.net',
            hotel_url='http://www.testhotelurl.com',
            hotel_description='some words',
            admin=user
        )
        hotel_data = {
            'hotel_name': 'hotel_test_2',
            'hotel_long': 3.000402,
            'hotel_lat': 3.000043,
            'hotel_email': 'emailfortesst@gmail.net',
            'hotel_url': 'http://www.testhotelurl.com',
            'hotel_description': 'some words',
        }
        form = AddHotelForm(data=hotel_data)
        error = {}
        for field in form.errors:
            error[field] = form.errors[field].as_text()

        self.assertFalse(form.is_valid())
        self.assertEquals(error['__all__'],
                          f'* Отель с сайтом {hotel_data["hotel_url"]} уже зарегистрирован!')

    def test_add_hotel_form_no_valid_hotel_long_lat(self):
        user = User.objects.get(username='tst')
        Hotel.objects.create(
            hotel_name='hotel_test',
            hotel_long=3.000002,
            hotel_lat=3.000003,
            hotel_email='emailfortest@gmail.net',
            hotel_url='http://www.testhotelurl.com',
            hotel_description='some words',
            admin=user
        )
        hotel_data = {
            'hotel_name': 'hotel_test_2',
            'hotel_long': 3.000002,
            'hotel_lat': 3.000003,
            'hotel_email': 'emailfortesst@gmail.net',
            'hotel_url': 'http://www.tesythotelurl.com',
            'hotel_description': 'some words',
        }
        form = AddHotelForm(data=hotel_data)
        error = {}
        for field in form.errors:
            error[field] = form.errors[field].as_text()

        self.assertFalse(form.is_valid())
        self.assertEquals(error['__all__'],
                          f'* Отель по координатам {hotel_data["hotel_lat"]}, {hotel_data["hotel_long"]} уже зарегистрирован!')

    def test_add_hotel_form_normal_data(self):
        hotel_data = {
            'hotel_name': 'hotel_test_2',
            'hotel_long': 3.000402,
            'hotel_lat': 3.000043,
            'hotel_email': 'secondsetuptest@gmail.net',
            'hotel_url': 'http://www.testhotelurl.com',
            'hotel_description': 'some words',
        }
        form = AddHotelForm(data=hotel_data)
        self.assertTrue(form.is_valid())

    def test_add_hotel_form_temp(self):
        hotel_data = {
            'hotel_name': '',
            'hotel_long': 342523452345,
            'hotel_lat': 342323452345,
            'hotel_email': 'bademail',
            'hotel_url': 'badurl',
            'hotel_description': 'some text',
        }
        form = AddHotelForm(data=hotel_data)
        errors_filed = {}
        for field in form.errors:
            errors_filed[field] = form.errors[field].as_text()
        self.assertEquals(errors_filed['hotel_long'],
                          '* Ensure that there are no more than 9 digits in total.')
        self.assertEquals(errors_filed['hotel_lat'],
                          '* Ensure that there are no more than 9 digits in total.')
        self.assertEquals(errors_filed['hotel_email'],
                          '* Enter a valid email address.')
        self.assertEquals(errors_filed['hotel_url'],
                          '* Enter a valid URL.')
        self.assertFalse(form.is_valid())


class TestAddRoomTypeRoom(TestCase):

    def setUp(self):
        self.client = Client()
        self.credentials = {
            'username': 'tst',
            'password': 'QazxsW1234'}
        admin = User.objects.create_user(**self.credentials)
        Admin.objects.create(user=admin)

        self.hotel = Hotel.objects.create(
            hotel_name='setup_hotel',
            hotel_long=3.000012,
            hotel_lat=3.000103,
            hotel_email='setuptest@gmail.ua',
            hotel_url='http://www.testhotelurlsetup.net',
            hotel_description='some words',
            admin=admin,
            url='setup_hotelHotel'
        )

        RoomTypes.objects.create(
            room_type_name='setup_room_type_name',
            room_type_description='setup description text',
            room_type_price=100,
            hotel=self.hotel
        )

    def test_add_room_type_normal_data(self):
        room_type_data = {
            'room_type_name': 'test_room_type',
            'room_type_description': 'some description text',
            'room_type_price': 100,
            'hotel': self.hotel,
        }
        form = AddRoomTypeForm(data=room_type_data)
        self.assertTrue(form.is_valid())

    def test_add_room_type_no_valid_name(self):
        room_type_data = {
            'room_type_name': 'setup_room_type_name',
            'room_type_description': 'some description text',
            'room_type_price': 100,
            'hotel': self.hotel,
        }
        form = AddRoomTypeForm(data=room_type_data)
        errors_filed = {}
        for field in form.errors:
            errors_filed[field] = form.errors[field].as_text()

        self.assertFalse(form.is_valid())
        self.assertEquals(errors_filed['__all__'],
                          f'* Room type with a name {room_type_data["room_type_name"]}  already exists!')

    def test_add_room_type_no_data(self):
        room_type_data = {
            'room_type_name': '',
            'room_type_description': '',
            'room_type_price': '',
            'hotel': None,
        }
        form = AddRoomTypeForm(data=room_type_data)
        errors_filed = {}
        for field in form.errors:
            errors_filed[field] = form.errors[field].as_text()
        self.assertEquals(errors_filed['room_type_name'],
                          '* This field is required.')
        self.assertEquals(errors_filed['room_type_description'],
                          '* This field is required.')
        self.assertEquals(errors_filed['room_type_price'],
                          '* This field is required.')

    def test_add_room_type_invalid_data(self):
        room_type_data = {
            'room_type_name': '',
            'room_type_description': '',
            'room_type_price': 14211234123412,
            'hotel': self.client,
        }
        form = AddRoomTypeForm(data=room_type_data)
        errors_filed = {}
        for field in form.errors:
            errors_filed[field] = form.errors[field].as_text()
        self.assertEquals(errors_filed['room_type_name'],
                          '* This field is required.')
        self.assertEquals(errors_filed['room_type_description'],
                          '* This field is required.')
        self.assertEquals(errors_filed['room_type_price'],
                          '* Ensure that there are no more than 6 digits in total.')
