# Generated by Django 3.2.5 on 2021-08-13 16:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotelcontent', '0005_auto_20210813_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookings',
            name='hotel_name_reserve',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='bookings',
            name='room_number_reserve',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='bookings',
            name='room',
            field=models.ForeignKey(default=0, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hotelcontent.rooms'),
        ),
    ]