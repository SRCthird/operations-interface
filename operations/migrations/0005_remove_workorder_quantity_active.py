# Generated by Django 4.2.6 on 2023-10-20 21:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0004_alter_workorder_actual_start_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workorder',
            name='quantity_active',
        ),
    ]