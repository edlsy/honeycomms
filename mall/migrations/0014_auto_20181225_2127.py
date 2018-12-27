# Generated by Django 2.1.4 on 2018-12-25 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mall', '0013_product_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='img',
        ),
        migrations.RemoveField(
            model_name='product',
            name='img_link',
        ),
        migrations.AddField(
            model_name='product',
            name='device_image_url',
            field=models.URLField(null=True),
        ),
    ]