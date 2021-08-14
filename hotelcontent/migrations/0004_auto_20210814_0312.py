# Generated by Django 3.2.5 on 2021-08-14 00:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelcontent', '0003_auto_20210813_2352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coefficient',
            name='end_date',
            field=models.DateField(default=datetime.date(2021, 8, 14)),
        ),
        migrations.AlterField(
            model_name='coefficient',
            name='start_date',
            field=models.DateField(default=datetime.date(2021, 8, 14)),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='hotel_image',
            field=models.ImageField(blank=True, null=True, upload_to='hotels'),
        ),
    ]