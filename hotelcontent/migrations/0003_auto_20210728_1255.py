# Generated by Django 3.2.5 on 2021-07-28 09:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotelcontent', '0002_agent_reservation_booking_status_bookings_hotel_room_types_rooms'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amenity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
            ],
        ),
        migrations.CreateModel(
            name='RoomTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel_type_name', models.CharField(max_length=200)),
                ('hotel_type_description', models.CharField(max_length=200)),
                ('hotel_type_price', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.RenameModel(
            old_name='Booking_status',
            new_name='AgentReservation',
        ),
        migrations.RenameModel(
            old_name='Agent_reservation',
            new_name='BookingStatus',
        ),
        migrations.RenameField(
            model_name='agentreservation',
            old_name='booking_status_description',
            new_name='agent_details',
        ),
        migrations.RenameField(
            model_name='bookings',
            old_name='from_date',
            new_name='checkin',
        ),
        migrations.RenameField(
            model_name='bookings',
            old_name='until_date',
            new_name='checkout',
        ),
        migrations.RenameField(
            model_name='bookingstatus',
            old_name='agent_details',
            new_name='booking_status_description',
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='hotel_address',
        ),
        migrations.RemoveField(
            model_name='rooms',
            name='room_rate',
        ),
        migrations.RemoveField(
            model_name='rooms',
            name='smoking_yn',
        ),
        migrations.AddField(
            model_name='bookings',
            name='rate_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
        migrations.AddField(
            model_name='hotel',
            name='hotel_description',
            field=models.TextField(default='...'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='hotel_lat',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=9),
        ),
        migrations.AddField(
            model_name='hotel',
            name='hotel_long',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=9),
        ),
        migrations.AddField(
            model_name='rooms',
            name='room_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='hotel_email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='hotel_url',
            field=models.URLField(),
        ),
        migrations.CreateModel(
            name='RateAmenity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amenity', models.ManyToManyField(to='hotelcontent.Amenity')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotelcontent.rooms')),
            ],
        ),
        migrations.CreateModel(
            name='Coef',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coef', models.DecimalField(decimal_places=2, max_digits=7)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotelcontent.hotel')),
            ],
        ),
        migrations.AlterField(
            model_name='rooms',
            name='room_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotelcontent.roomtypes'),
        ),
        migrations.DeleteModel(
            name='Room_types',
        ),
    ]
