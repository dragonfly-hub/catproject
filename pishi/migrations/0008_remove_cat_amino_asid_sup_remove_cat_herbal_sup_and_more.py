# Generated by Django 5.1.2 on 2024-10-30 18:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pishi', '0007_delete_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cat',
            name='amino_asid_sup',
        ),
        migrations.RemoveField(
            model_name='cat',
            name='herbal_sup',
        ),
        migrations.RemoveField(
            model_name='cat',
            name='mineral_sup',
        ),
        migrations.RemoveField(
            model_name='cat',
            name='omega_sup',
        ),
        migrations.RemoveField(
            model_name='cat',
            name='probiotic_sup',
        ),
        migrations.RemoveField(
            model_name='cat',
            name='vitamin_sup',
        ),
    ]