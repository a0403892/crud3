# Generated by Django 5.0.1 on 2024-02-16 17:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crudpractice', '0029_rename_myimagemodel_photomodel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='datelast',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 16, 17, 27, 1, 367278, tzinfo=datetime.timezone.utc)),
        ),
    ]