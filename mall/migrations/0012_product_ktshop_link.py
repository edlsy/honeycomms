# Generated by Django 2.1.4 on 2018-12-17 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mall', '0011_auto_20181217_0140'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='ktshop_link',
            field=models.CharField(default='', max_length=200),
        ),
    ]