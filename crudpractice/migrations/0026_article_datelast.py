# Generated by Django 5.0.1 on 2024-02-16 07:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crudpractice', '0025_rename_date_article_datestart'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='datelast',
            field=models.DateField(default=datetime.datetime(2024, 2, 16, 7, 43, 2, 74915, tzinfo=datetime.timezone.utc)),
        ),
    ]