# Generated by Django 3.0.7 on 2020-06-16 11:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20200612_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 6, 16, 11, 41, 38, 699210, tzinfo=utc)),
        ),
    ]
