# Generated by Django 5.1.2 on 2024-11-19 16:25

import django.contrib.auth.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catlog', '0004_comment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name=django.contrib.auth.models.User)),
                ('biography', models.TextField(blank=True, default='', max_length=200, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='upload/users_profile/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='catlog_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catlog.profile'),
        ),
    ]
