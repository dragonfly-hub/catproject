# Generated by Django 5.1.2 on 2024-11-29 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shippingaddress',
            options={'verbose_name_plural': 'Shipping Address'},
        ),
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='Full_name',
            new_name='full_name',
        ),
    ]
