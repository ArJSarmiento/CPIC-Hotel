# Generated by Django 3.2.8 on 2021-12-26 12:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelSystem', '0017_auto_20211226_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkin',
            name='check_in_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 26, 20, 11, 8, 661542)),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='last_edited_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 26, 20, 11, 8, 661542)),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='expected_arrival_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 26, 20, 11, 8, 659538)),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='expected_departure_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 26, 20, 11, 8, 659538)),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='reservation_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 26, 20, 11, 8, 659538)),
        ),
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Others')], default='Others', max_length=1),
        ),
    ]
