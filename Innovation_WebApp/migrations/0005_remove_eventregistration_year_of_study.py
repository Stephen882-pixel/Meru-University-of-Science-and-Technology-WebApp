# Generated by Django 5.1.3 on 2024-12-07 05:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Innovation_WebApp', '0004_eventregistration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventregistration',
            name='year_of_study',
        ),
    ]