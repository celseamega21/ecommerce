# Generated by Django 5.1.6 on 2025-03-06 18:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_rename_payments_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='total',
        ),
    ]
