# Generated by Django 3.2.5 on 2021-08-04 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelcontent', '0020_auto_20210804_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookings',
            name='checkin',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='bookings',
            name='checkout',
            field=models.DateField(),
        ),
    ]