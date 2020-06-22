# Generated by Django 3.0.7 on 2020-06-21 14:25

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_auto_20200621_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packagecontent',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='package_content', to='products.Package'),
        ),
        migrations.AlterField(
            model_name='product',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 6, 21, 14, 25, 52, 85921, tzinfo=utc)),
        ),
    ]
