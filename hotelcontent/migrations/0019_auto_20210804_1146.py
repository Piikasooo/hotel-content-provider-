# Generated by Django 3.2.5 on 2021-08-04 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotelcontent', '0018_auto_20210804_1145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookings',
            name='hotels',
        ),
        migrations.AddField(
            model_name='bookings',
            name='hotels',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='hotelcontent.hotel'),
        ),
    ]
