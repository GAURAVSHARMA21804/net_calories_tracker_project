# Generated by Django 5.1.3 on 2024-12-01 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='last_calculated_bmr',
            field=models.FloatField(blank=True, help_text='Cached BMR value', null=True),
        ),
    ]
