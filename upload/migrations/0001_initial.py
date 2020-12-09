# Generated by Django 3.1.3 on 2020-11-27 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UploadFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload_file', models.FileField(upload_to='files/')),
            ],
            options={
                'verbose_name': 'Upload Files',
                'verbose_name_plural': 'Upload Files',
            },
        ),
    ]
