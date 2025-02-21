# Generated by Django 5.1.3 on 2025-02-05 10:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Innovation_WebApp', '0017_alter_eventregistration_uid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventregistration',
            name='uid',
        ),
        migrations.AlterField(
            model_name='eventregistration',
            name='email',
            field=models.EmailField(max_length=254, primary_key=True, serialize=False, validators=[django.core.validators.EmailValidator()]),
        ),
        migrations.AlterField(
            model_name='eventregistration',
            name='ticket_number',
            field=models.CharField(blank=True, max_length=50, unique=True),
        ),
    ]
