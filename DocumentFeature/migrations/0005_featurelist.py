# Generated by Django 3.1.3 on 2021-02-10 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DocumentFeature', '0004_auto_20210210_1741'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeatureList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]
