# Generated by Django 3.0.7 on 2020-06-26 11:24

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_auto_20200626_0813'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddonItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('quantity_available', models.PositiveIntegerField(default=1)),
                ('available', models.BooleanField(default=True)),
                ('created', models.DateTimeField(blank=True, default=datetime.datetime(2020, 6, 26, 11, 24, 1, 526463, tzinfo=utc))),
            ],
        ),
        migrations.RemoveConstraint(
            model_name='productaddon',
            name='unique_combination',
        ),
        migrations.RemoveField(
            model_name='productaddon',
            name='food_item',
        ),
        migrations.AlterField(
            model_name='product',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 6, 26, 11, 24, 1, 478779, tzinfo=utc)),
        ),
        migrations.DeleteModel(
            name='FoodItem',
        ),
        migrations.AddField(
            model_name='productaddon',
            name='add_on_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.AddonItem'),
        ),
    ]