# Generated by Django 3.0.5 on 2020-05-14 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('file_id', models.AutoField(primary_key=True, serialize=False)),
                ('file', models.FileField(max_length=255, null=True, upload_to='')),
            ],
        ),
    ]