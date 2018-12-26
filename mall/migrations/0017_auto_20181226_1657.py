# Generated by Django 2.1.4 on 2018-12-26 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mall', '0016_auto_20181226_0046'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='is_active',
            new_name='on_sale',
        ),
        migrations.RemoveField(
            model_name='product_color',
            name='is_active',
        ),
        migrations.AddField(
            model_name='product_color',
            name='on_sale',
            field=models.BooleanField(default=False),
        ),
    ]
