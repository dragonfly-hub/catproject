# Generated by Django 5.1.2 on 2024-10-29 17:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catshop', '0007_product_star_alter_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 10, 29, 21, 17, 18, 207675)),
        ),
    ]
