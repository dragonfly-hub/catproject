# Generated by Django 5.1.2 on 2024-12-10 17:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catshop', '0029_alter_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 12, 10, 20, 36, 7, 544546)),
        ),
    ]
