# Generated by Django 2.1.4 on 2018-12-15 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mall', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='code',
            new_name='device_code',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='name',
            new_name='device_name',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='price',
            new_name='device_price',
        ),
    ]