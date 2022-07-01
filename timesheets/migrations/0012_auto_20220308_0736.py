# Generated by Django 3.0 on 2022-03-08 12:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0011_auto_20220308_0643'),
    ]

    operations = [
        migrations.AddField(
            model_name='master_db',
            name='week_end',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='master_db',
            name='week_start',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
        ),
    ]