# Generated by Django 3.2.5 on 2021-08-13 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelcontent', '0008_auto_20210813_2257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookings',
            name='room_number_reserve',
            field=models.IntegerField(blank=True),
        ),
    ]