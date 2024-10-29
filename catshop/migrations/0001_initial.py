# Generated by Django 5.1.2 on 2024-10-29 13:07

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=100)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('description', models.CharField(blank=True, default='', max_length=500, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('picture', models.ImageField(upload_to='upload/product/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catshop.category')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('address', models.CharField(blank=True, default='', max_length=400)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('date', models.DateField(default=datetime.datetime(2024, 10, 29, 16, 37, 36, 365414))),
                ('status', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catshop.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catshop.product')),
            ],
        ),
    ]
