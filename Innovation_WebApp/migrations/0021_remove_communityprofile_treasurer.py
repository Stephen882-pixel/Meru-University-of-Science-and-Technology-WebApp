# Generated by Django 5.1.3 on 2025-02-06 08:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Innovation_WebApp', '0020_alter_eventregistration_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='communityprofile',
            name='treasurer',
        ),
    ]
