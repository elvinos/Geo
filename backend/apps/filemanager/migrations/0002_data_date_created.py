# Generated by Django 3.0.5 on 2020-05-14 09:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('filemanager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
