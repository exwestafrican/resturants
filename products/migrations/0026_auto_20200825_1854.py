# Generated by Django 3.0.7 on 2020-08-25 17:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0025_auto_20200825_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addonitem',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 8, 25, 17, 54, 59, 735318, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='product',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 8, 25, 17, 54, 59, 702623, tzinfo=utc)),
        ),
    ]