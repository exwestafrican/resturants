# Generated by Django 3.0.7 on 2020-06-13 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='name',
        ),
        migrations.AddField(
            model_name='cart',
            name='cart_id',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
