# Generated by Django 5.1.2 on 2024-11-19 16:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catshop', '0021_profile_old_cart_alter_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 11, 19, 19, 55, 51, 59252)),
        ),
    ]