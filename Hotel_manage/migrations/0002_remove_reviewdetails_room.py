# Generated by Django 4.2.3 on 2023-07-28 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hotel_manage', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewdetails',
            name='room',
        ),
    ]
