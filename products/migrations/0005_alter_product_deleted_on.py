# Generated by Django 3.2.25 on 2024-12-17 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_deleted_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='deleted_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
