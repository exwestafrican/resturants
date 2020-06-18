# Generated by Django 3.0.7 on 2020-06-18 16:52

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20200618_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 6, 18, 16, 52, 6, 539205, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.ProductVariation'),
        ),
    ]