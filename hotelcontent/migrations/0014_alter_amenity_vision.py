# Generated by Django 3.2.5 on 2021-08-01 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelcontent', '0013_alter_amenity_vision'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amenity',
            name='vision',
            field=models.BooleanField(default=True),
        ),
    ]
