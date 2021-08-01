# Generated by Django 3.2.5 on 2021-07-29 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotelcontent', '0004_delete_rateamenity'),
    ]

    operations = [
        migrations.CreateModel(
            name='RateAmenity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amenity', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='hotelcontent.amenity', verbose_name='Amenity')),
                ('room', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='hotelcontent.rooms', verbose_name='Комната')),
            ],
        ),
    ]