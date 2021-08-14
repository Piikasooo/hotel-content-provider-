# Generated by Django 3.2.5 on 2021-08-13 07:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelcontent', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookings',
            name='hotels',
        ),
        migrations.AddField(
            model_name='bookings',
            name='hotel',
            field=models.CharField(default='OdessaHotel', max_length=200),
        ),
        migrations.AlterField(
            model_name='bookings',
            name='room',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='coefficient',
            name='end_date',
            field=models.DateField(default=datetime.date(2021, 8, 13)),
        ),
        migrations.AlterField(
            model_name='coefficient',
            name='start_date',
            field=models.DateField(default=datetime.date(2021, 8, 13)),
        ),
    ]
