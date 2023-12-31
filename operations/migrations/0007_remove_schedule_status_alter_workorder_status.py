# Generated by Django 4.2.6 on 2023-10-20 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0006_workorder_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='status',
        ),
        migrations.AlterField(
            model_name='workorder',
            name='status',
            field=models.CharField(choices=[('1', 'Released'), ('2', 'In Progress'), ('3', 'On Hold'), ('4', 'Rework'), ('5', 'Lot Release'), ('6', 'Scrapped'), ('7', 'Completed')], default='Scheduled', max_length=25),
        ),
    ]
