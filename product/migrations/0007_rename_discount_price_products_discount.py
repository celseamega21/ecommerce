# Generated by Django 5.1.6 on 2025-02-21 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_alter_products_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='products',
            old_name='discount_price',
            new_name='discount',
        ),
    ]
