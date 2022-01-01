# Generated by Django 3.2.8 on 2021-11-12 07:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelSystem', '0002_auto_20211104_2111'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='sex',
            field=models.CharField(choices=[('F', 'Female'), ('M', 'Male'), ('O', 'Others')], default='Others', max_length=1),
        ),
        migrations.AddField(
            model_name='user',
            name='sex',
            field=models.CharField(choices=[('F', 'Female'), ('M', 'Male'), ('O', 'Others')], default='Others', max_length=1),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='expected_arrival_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 12, 15, 51, 4, 653066)),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='expected_departure_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 12, 15, 51, 4, 653066)),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='reservation_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 12, 15, 51, 4, 653066)),
        ),
    ]
