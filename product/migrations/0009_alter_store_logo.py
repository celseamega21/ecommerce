# Generated by Django 5.1.6 on 2025-02-26 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_alter_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='logo',
            field=models.ImageField(blank=True, default='store_logo/Screenshot_12.png', null=True, upload_to='store_logo/'),
        ),
    ]
