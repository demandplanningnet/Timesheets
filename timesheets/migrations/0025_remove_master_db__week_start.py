# Generated by Django 3.0 on 2022-06-27 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0024_master_db__week_start'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='master_db',
            name='_week_start',
        ),
    ]
