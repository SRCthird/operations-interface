# Generated by Django 4.2.6 on 2023-10-21 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0007_remove_schedule_status_alter_workorder_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='request_type',
            field=models.CharField(choices=[(1, 'New Lot'), (2, 'New Rack'), (3, 'Replacement Rack'), (4, 'Project Lot')], max_length=25),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='status',
            field=models.CharField(choices=[(1, 'Released'), (2, 'In Progress'), (3, 'On Hold'), (4, 'Rework'), (5, 'Lot Release'), (6, 'Scrapped'), (7, 'Completed')], default='Scheduled', max_length=25),
        ),
    ]
