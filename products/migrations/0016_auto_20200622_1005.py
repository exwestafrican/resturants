# Generated by Django 3.0.7 on 2020-06-22 09:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_auto_20200622_1004'),
    ]

    operations = [
        migrations.RenameField(
            model_name='packagecontent',
            old_name='content',
            new_name='product',
        ),
        migrations.AlterField(
            model_name='product',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 6, 22, 9, 5, 31, 824395, tzinfo=utc)),
        ),
    ]
