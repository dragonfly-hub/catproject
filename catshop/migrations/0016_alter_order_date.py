# Generated by Django 5.1.2 on 2024-10-30 21:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catshop', '0015_alter_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 10, 31, 0, 53, 55, 108143)),
        ),
    ]
