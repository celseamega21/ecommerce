# Generated by Django 5.1.6 on 2025-02-19 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('ADMIN', 'Admin'), ('SELLER', 'Seller'), ('BUYER', 'Buyer')], default='BUYER', max_length=10),
        ),
    ]
