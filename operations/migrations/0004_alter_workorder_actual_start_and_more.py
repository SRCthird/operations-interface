# Generated by Django 4.2.6 on 2023-10-20 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0003_alter_workorder_actual_start_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorder',
            name='actual_start',
            field=models.DateField(blank=True, help_text='The actual start date of the workorder.', null=True),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='quantity_active',
            field=models.IntegerField(blank=True, help_text='Living quantity of units as it progresses through the lines.', null=True),
        ),
    ]
