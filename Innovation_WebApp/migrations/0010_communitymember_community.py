# Generated by Django 5.1.3 on 2024-12-08 15:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Innovation_WebApp', '0009_remove_communitymember_community'),
    ]

    operations = [
        migrations.AddField(
            model_name='communitymember',
            name='community',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='members', to='Innovation_WebApp.communityprofile'),
        ),
    ]
