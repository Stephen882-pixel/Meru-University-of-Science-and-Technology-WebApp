# Generated by Django 5.1.3 on 2024-12-21 06:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Innovation_WebApp', '0010_communitymember_community'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='communityprofile',
            name='total_members',
        ),
    ]
