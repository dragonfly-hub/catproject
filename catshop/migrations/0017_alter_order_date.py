# Generated by Django 5.1.2 on 2024-10-30 21:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catshop', '0016_alter_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 10, 31, 1, 1, 11, 603254)),
        ),
    ]
