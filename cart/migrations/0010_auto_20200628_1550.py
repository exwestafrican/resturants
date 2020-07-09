# Generated by Django 3.0.7 on 2020-06-28 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0009_cart_bought'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='bought',
        ),
        migrations.AddField(
            model_name='cart',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]