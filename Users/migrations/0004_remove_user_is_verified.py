# Generated by Django 3.1.3 on 2021-01-12 10:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_subscription'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_verified',
        ),
    ]
