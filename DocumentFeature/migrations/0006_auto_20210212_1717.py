# Generated by Django 3.1.3 on 2021-02-12 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DocumentFeature', '0005_featurelist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultfeature',
            name='body',
            field=models.TextField(),
        ),
    ]
