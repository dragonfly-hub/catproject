# Generated by Django 5.1.2 on 2024-11-29 13:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catshop', '0025_alter_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 11, 29, 17, 25, 31, 900812)),
        ),
    ]