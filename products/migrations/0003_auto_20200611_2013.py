# Generated by Django 3.0.7 on 2020-06-11 20:13

from django.db import migrations, models
import products.utils


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20200611_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(blank=True, null=True, unique=True, upload_to=products.utils.image_path),
        ),
    ]
