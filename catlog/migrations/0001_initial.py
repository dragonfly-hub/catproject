# Generated by Django 5.1.2 on 2024-10-15 18:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_name', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=250)),
                ('excerpt', models.TextField(blank=True, default='', max_length=500, null=True)),
                ('body', models.TextField()),
                ('date', models.DateField(default=datetime.date.today)),
                ('picture', models.ImageField(upload_to='upload/%y/%m/%d')),
            ],
        ),
    ]
