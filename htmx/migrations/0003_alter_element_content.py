# Generated by Django 4.2.6 on 2023-10-22 20:55

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('htmx', '0002_alter_element_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='element',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
