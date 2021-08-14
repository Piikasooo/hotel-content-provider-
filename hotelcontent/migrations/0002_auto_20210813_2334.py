# Generated by Django 3.2.5 on 2021-08-13 20:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotelcontent', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HotelsImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel_photo', models.ImageField(null=True, upload_to='')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotelcontent.hotel')),
            ],
        ),
        migrations.DeleteModel(
            name='RoomImages',
        ),
    ]
